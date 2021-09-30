import asyncio
import json
from threading import Thread
import zmq

class WebsocketUpdater(Thread):
    def __init__(self, context, clients):
        super(WebsocketUpdater, self).__init__()
        self.context = context
        self.light_pull_socket = context.socket(zmq.PULL)
        self.light_pull_socket.connect('inproc://lightstream')

        self.clients = clients

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            event = self.light_pull_socket.recv_json()
            for client in self.clients:
                client.write_message(json.dumps(event))