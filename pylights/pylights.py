import zmq
from lightcontroller import LightController
from websocketupdater import WebsocketUpdater
from webserver import WebService

clients = []
context = zmq.Context()

def main():
    light_controller = LightController(context)
    webserver = WebService(context, clients)
    websocket_updater = WebsocketUpdater(context, clients)

    light_controller.start()
    webserver.start()
    websocket_updater.start()

if __name__ == "__main__" :
    main()
