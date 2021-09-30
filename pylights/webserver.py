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
    def __init__(self, context, clients):
        super(WebService, self).__init__()
        self.context = context
        self.clients = clients

        self.light_req_socket = context.socket(zmq.REQ)
        self.light_req_socket.connect('inproc://weblights')

        self.app = WebServer(self.clients, self.light_req_socket)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        tornado.options.parse_command_line()
        print(f'WebServer listening on port {options.port}')
        self.app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

class WebServer(tornado.web.Application):
    def __init__(self, clients, light_req_socket):
        self.clients = clients
        self.light_req_socket = light_req_socket
        handlers = [
            (r"/lightsocket", LightsWebSocket, {
                'clients': self.clients,
                'light_req_socket': self.light_req_socket}),
            (r"/api", RestHandler),
            (r"/api/nextturn", NextTurnHandler, {'light_req_socket': self.light_req_socket}),
            (r"/api/startgame", StartGameHandler, {'light_req_socket': self.light_req_socket})
        ]
        super().__init__(handlers, {})

class LightsWebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, clients, light_req_socket):
        self.clients = clients
        self.light_req_socket = light_req_socket

    def check_origin(self, origin):
        return True

    def open(self):
        self.clients.append(self)
        print(f"WebSocket opened from {self.request.host}")
        command = {'command': 'getlights'}
        self.light_req_socket.send_json(command)
        res = self.light_req_socket.recv_json()
        self.write_message(json.dumps(res))

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
    def initialize(self, light_req_socket):
        self.light_req_socket = light_req_socket

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self):
        print('going to next turn')
        command = {'command': 'nextturn'}
        self.light_req_socket.send_json(command)
        self.light_req_socket.recv()

class StartGameHandler(tornado.web.RequestHandler):
    def initialize(self, light_req_socket):
        self.light_req_socket = light_req_socket

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
        self.light_req_socket.send_json(command)
        self.light_req_socket.recv()