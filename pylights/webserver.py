import asyncio
import json
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import zmq
from tornado.options import define, options

COMMAND_TOPIC = 'command'

define("port", default=8756, type=int)

class WebService(threading.Thread):
    def __init__(self, context, lights):
        super(WebService, self).__init__()
        self.context = zmq.Context()
        self.lights = lights
        self.light_controller_socket = context.socket(zmq.PAIR)
        # Connect to LightController server (used to send bi-directional light updates)
        self.light_controller_socket.connect('inproc://weblights')
        self.web_req_socket = context.socket(zmq.REQ)
        # Connect to LightController client (used to get initial light status)
        self.web_req_socket.bind('inproc://webreq')
        self.app = WebServer(self.light_controller_socket, self.web_req_socket, lights)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        tornado.options.parse_command_line()
        print(f'WebServer listening on port {options.port}')
        self.app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

class WebServer(tornado.web.Application):
    def __init__(self, light_controller_socket, web_req_socket, lights):
        self.clients = []
        self.lights = lights
        self.light_controller_socket = light_controller_socket
        self.web_req_socket = web_req_socket
        handlers = [
            (r"/lightsocket", LightsWebSocket, {
                'clients': self.clients,
                'light_controller_socket': self.light_controller_socket,
                'web_req_socket': self.web_req_socket,
                'lights': self.lights}),
            (r"/api", RestHandler),
            (r"/api/nextturn", NextTurnHandler, {'light_controller_socket': self.light_controller_socket}),
            (r"/api/startgame", StartGameHandler, {'light_controller_socket': self.light_controller_socket})
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
    def initialize(self, clients, light_controller_socket, web_req_socket, lights):
        self.clients = clients
        self.lights = lights
        self.light_controller_socket = light_controller_socket
        self.web_req_socket = web_req_socket

    def check_origin(self, origin):
        return True

    def open(self):
        self.clients.append(self)
        print(f'lights: {self.lights}')
        print(f"WebSocket opened from {self.request.host}")
        self.write_message(json.dumps(self.lights))

    def on_close(self):
        self.clients.remove(self)
        print(f"WebSocket closed from {self.request.host}")

class RestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self):
        self.write(json.dumps({
            'message': 'hello'
        }))

class NextTurnHandler(tornado.web.RequestHandler):
    def initialize(self, light_controller_socket):
        self.light_controller_socket = light_controller_socket

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self):
        print('going to next turn')
        command = {'command': 'nextturn'}
        self.light_controller_socket.send_string(f'{COMMAND_TOPIC} {json.dumps(command)}')

class StartGameHandler(tornado.web.RequestHandler):
    def initialize(self, light_controller_socket):
        self.light_controller_socket = light_controller_socket

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print(f'starting new game: {data}')
        command = {
            'command': 'startgame',
            'players': data
        }
        print(f'post command to queue: {json.dumps(command)}')
        self.light_controller_socket.send_string(f'{COMMAND_TOPIC} {json.dumps(command)}')