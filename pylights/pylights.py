import json
import random
import asyncio
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options
from threading import Thread
import time
import zmq

LIGHTS_TOPIC = 'update_lights'
NUM_LIGHTS = 148

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('inproc://#1')
sub_socket = context.socket(zmq.SUB)
sub_socket.setsockopt(zmq.SUBSCRIBE, LIGHTS_TOPIC.encode())
sub_socket.connect('inproc://#1')


clients = []
global_lights = []
players = []
define("port", default=8756, type=int)

class WebServer(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/lightsocket", LightsWebSocket),
            (r"/api", RestHandler)
        ]
        super().__init__(handlers, {})

    def signal_handler(self, signum, frame):
        print('exiting...')
        self.is_closing = True
        raise Exception('quitting')
    
    def try_exit(self):
        if self.is_closing:
            tornado.ioloop.IOLoop.instance().stop()
            print('exited')

class LightsWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        global global_lights
        clients.append(self)
        print(f"WebSocket opened from {self.request.host}")
        self.write_message(json.dumps(global_lights))
    
    # def on_message(self, message):
    #     print(f"Received message: {message}")
    #     self.write_message(f'You said: {message}')
    
    def on_close(self):
        clients.remove(self)
        print(f"WebSocket closed from {self.request.host}")

class RestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self):
        self.write(json.dumps({
            'message': 'hello'
        }))

def update_lights():
    pub_socket.send_string(f'{LIGHTS_TOPIC} {json.dumps(global_lights)}')

def init_lights(rgb=(0,0,0)):
    global global_lights
    global_lights = []

    for num in range(NUM_LIGHTS):
        global_lights.append({
            'r': rgb[0],
            'g': rgb[1],
            'b': rgb[2]
        })

# Set all lights to random colors
def lights_random(delay=0.5) :
    global global_lights
    while True:
        for light in global_lights:
            light['r'] = random.randint(0,255)
            light['g'] = random.randint(0,255)
            light['b'] = random.randint(0,255)
        update_lights()
        time.sleep(delay)

def lights_off() :
    global global_lights
    for light in global_lights:
        light['r'] = 0
        light['g'] = 0
        light['b'] = 0
    update_lights()

# Light up one at a time sequentially
def lights_on_sequential(rgb=(0,0,0), delay=0.03):
    global global_lights
    while True:
        for i in range(len(global_lights)):
            global_lights[i]['r'] = rgb[0]
            global_lights[i]['g'] = rgb[1]
            global_lights[i]['b'] = rgb[2]
            global_lights[i-1]['r'] = 0
            global_lights[i-1]['g'] = 0
            global_lights[i-1]['b'] = 0
            update_lights()
            time.sleep(delay)

# Light up sequentially as a train, cycle through colors
def lights_on_sequential_rgb(delay=.02, colors = [(255,0,0),(0,255,0),(0,0,255)]):
    global global_lights
    while True:
        for color in colors:
            for light in global_lights:
                light['r'] = color[0]
                light['g'] = color[1]
                light['b'] = color[2]
                update_lights()
                time.sleep(delay)

# Blink all lights together
def blink_lights(delay=0.5, color=(255,0,0)):
    global global_lights
    while True:
        lights_off()
        for light in global_lights:
            light['r'] = color[0]
            light['g'] = color[1]
            light['b'] = color[2]
        time.sleep(delay)
        update_lights()
        time.sleep(delay)

def event_subscriber() :
    asyncio.set_event_loop(asyncio.new_event_loop())
    while (True) :
        event = sub_socket.recv().decode('utf-8').split()
        message = ''.join(event[1:])
        # print(f'sending light change to websocket!!!!!!!!!')
        send_to_websocket(message)

def send_to_websocket(message):
    for client in clients:
        # print('writing message to client')
        client.write_message(message)
        # print('wrote message to client')

def start_webserver():
    asyncio.set_event_loop(asyncio.new_event_loop())
    tornado.options.parse_command_line()
    app = WebServer()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

def main():
    init_lights()
    # lights_thread = Thread(target = lights_random, args=[0.1])
    # lights_thread = Thread(target = lights_on_sequential, args=[(255,0,0)])
    # lights_thread = Thread(target = lights_on_sequential_rgb)
    lights_thread = Thread(target = blink_lights)
    queue_listener_thread = Thread(target = event_subscriber)
    webserver_thread = Thread(target = start_webserver)

    webserver_thread.start()
    queue_listener_thread.start()
    lights_thread.start()

if __name__ == "__main__" :
    main()
