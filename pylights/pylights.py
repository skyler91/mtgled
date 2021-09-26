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

def init_random_lights(num_lights):
    lights = []
    for num in range(num_lights):
        lights.append({
            'r': random.randint(0, 255),
            'g': random.randint(0, 255),
            'b': random.randint(0,255)
        })
    return lights

def light_changer() :
    global global_lights
    num = 1
    while True:
        global_lights = init_random_lights(148)
        #print(f'changing lights')
        pub_socket.send_string(f'{LIGHTS_TOPIC} {json.dumps(global_lights)}')
        num += 1
        time.sleep(0.5)
        
def serve() :
    asyncio.set_event_loop(asyncio.new_event_loop())
    while (True) :
        event = sub_socket.recv().decode('utf-8').split()
        topic = event[0]
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
    t1 = Thread(target = light_changer)
    t2 = Thread(target = serve)
    t3 = Thread(target = start_webserver)
    t3.start()
    t1.start()
    t2.start()

if __name__ == "__main__" :
    main()