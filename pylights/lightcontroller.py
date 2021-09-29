import asyncio
import json
import random
import threading
import zmq

NUM_LIGHTS = 148
LIGHTS_TOPIC = 'update_lights'


class LightController(threading.Thread):
    def __init__(self, context, lights):
        super(LightController, self).__init__()
        self.context = zmq.Context()
        self.lights = lights
        self.web_controller_socket = context.socket(zmq.PAIR)
        self.web_controller_socket.bind('inproc://weblights')
        self.web_resp_socket = context.socket(zmq.REP)
        self.web_resp_socket.connect('inproc://webreq')
        self.init_lights((255,0,0))
        self.player_lights = {
        1: (0,25),
        2: (25,50),
        3: (50,74),
        4: (74,99),
        5: (99,124),
        6: (124,148)}

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while (True) :
            event =  self.web_controller_socket.recv().decode('utf-8')
            event_body = ''.join(event.split()[1:])
            print(f'got event: {event_body}')
            body = json.loads(event_body)
            print(body)
            if body['command'] == 'nextturn':
                self.lights_per_player()
            if body['command'] == 'startgame':
                global players
                global current_player
                print(f'body: {body}')
                players = body['players']
                current_player = 0
                self.lights_per_player()

    def init_lights(self, rgb=(0,0,0)):
        for num in range(NUM_LIGHTS):
            self.lights.append({
                'r': rgb[0],
                'g': rgb[1],
                'b': rgb[2]
            })

    def update_all_lights(self, rgb=(0,0,0)):
        for light in self.lights:
            light['r'] = rgb[0]
            light['g'] = rgb[1]
            light['b'] = rgb[2]

    def lights_per_player(self, rgb=(0,0,0), delay=2):
        print('called lights_per_player')
        self.update_all_lights((0,0,255))
        # global global_lights
        # global current_player
        # current_player = get_next_player()
        # print(f'current player set to {current_player}')
        # lights_off()
        # for l in range(player_lights[current_player][0], player_lights[current_player][1]):
        #     if rgb[0] == 0 and rgb[1] == 0 and rgb[2] == 0 :
        #         global_lights[l]['r'] = random.randint(0,255)
        #         global_lights[l]['g'] = random.randint(0,255)
        #         global_lights[l]['b'] = random.randint(0,255)
        #     else:
        #         global_lights[l]['r'] = rgb[0]
        #         global_lights[l]['g'] = rgb[1]
        #         global_lights[l]['b'] = rgb[2]
        # update_lights()