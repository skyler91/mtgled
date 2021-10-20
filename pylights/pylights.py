import zmq
from gamecontroller import GameController
from websocketupdater import WebsocketUpdater
from webserver import WebService

clients = []
context = zmq.Context()

def main():
    light_controller = GameController(context)
    webserver = WebService(context, clients)
    websocket_updater = WebsocketUpdater(context, clients)

    light_controller.start()
    webserver.start()
    websocket_updater.start()

if __name__ == "__main__" :
    main()
