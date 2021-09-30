import asyncio
import random
import threading
import time
import zmq

NUM_LIGHTS = 148
LIGHTS_TOPIC = 'update_lights'

class LightController(threading.Thread):
    def __init__(self, context):
        super(LightController, self).__init__()
        self.context = context
        self.light_rep_socket = context.socket(zmq.REP)
        self.light_rep_socket.bind('inproc://weblights')
        self.light_push_socket = context.socket(zmq.PUSH)
        self.light_push_socket.bind('inproc://lightstream')

        self.players = []
        self.current_player = 0

        self.lights = self.init_lights()
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
            event =  self.light_rep_socket.recv_json()
            print(f'got event: {event}')
            if event['command'] == 'getlights':
                self.light_rep_socket.send_json(self.lights)
            elif event['command'] == 'nextturn':
                self.next_turn()
                self.light_rep_socket.send_json(self.lights)
            elif event['command'] == 'startgame':
                self.new_game(event['players'])
                self.light_rep_socket.send_json(self.lights)
            else:
                self.light_rep_socket.send_json({'result': 'failed'})

    def init_lights(self, rgb=(0,0,0)):
        lights = []
        for num in range(NUM_LIGHTS):
            lights.append({
                'r': rgb[0],
                'g': rgb[1],
                'b': rgb[2]
            })
        return lights

    def new_game(self, players):
        self.players = players
        self.current_player = 0
        for i in range(1):
            self.lights_random()
            time.sleep(0.5)

    def update_all_lights(self, rgb=(0,0,0)):
        for light in self.lights:
            light['r'] = rgb[0]
            light['g'] = rgb[1]
            light['b'] = rgb[2]
        self.push_lights()

    def update_lights(self, light_indices, rgb=(0,0,0)):
        for light_index in light_indices:
            self.lights[light_index]['r'] = rgb[0]
            self.lights[light_index]['g'] = rgb[1]
            self.lights[light_index]['b'] = rgb[2]
        self.push_lights()

    def get_next_player(self):
        if self.current_player == 0:
            return self.players[0]

        next_player_index = self.players.index(self.current_player) + 1
        if next_player_index >= len(self.players):
            next_player_index = 0
        return self.players[next_player_index]

    def push_lights(self):
        print('publishing lights')
        self.light_push_socket.send_json(self.lights)

    def next_turn(self):
        self.current_player = self.get_next_player()
        print(f'current player: {self.current_player}')
        self.lights_off()
        self.update_lights(
            list(range(self.player_lights[self.current_player][0], self.player_lights[self.current_player][1])),
            (0,255,0))

    def lights_off(self) :
        self.update_all_lights()

    def lights_per_player(self, rgb=(0,0,0), delay=2):
        print('called lights_per_player')
        self.update_all_lights((0,255,0))
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

    # Set all lights to random colors
    def lights_random(self) :
        for light in self.lights:
            light['r'] = random.randint(0,255)
            light['g'] = random.randint(0,255)
            light['b'] = random.randint(0,255)
        self.push_lights()