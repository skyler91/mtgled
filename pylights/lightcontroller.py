import asyncio
import copy
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
        self.game_in_progress = False

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
            # print(f'got event: {event}')
            if event['command'] == 'getlights':
                self.light_rep_socket.send_json({
                    'status': self.game_in_progress,
                    'lights': self.rgb_to_hex()
                })
            elif event['command'] == 'nextturn':
                self.next_turn()
                self.light_rep_socket.send_json({
                    'status': self.game_in_progress,
                    'lights': self.rgb_to_hex()
                })
            elif event['command'] == 'startgame':
                self.new_game(event['players'])
                self.light_rep_socket.send_json({
                    'status': self.game_in_progress,
                    'lights': self.rgb_to_hex()
                    })
            else:
                self.light_rep_socket.send_json({'status': f'invalid command: {event.get("command")}'})

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
        # Ensure player numbers are integers
        self.players = list(map(lambda p : int(p), players))
        print(f'starting new game with players {players}')
        self.current_player = 0
        self.blink_lights()
        self.game_in_progress = True
        self.next_turn()

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

    def rgb_to_hex(self):
        hex_lights = []
        for light in self.lights:
            hex_lights.append('#%02x%02x%02x' % (light['r'], light['g'], light['b']))
        return hex_lights

    def push_lights(self):
        self.light_push_socket.send_json({
            'status': self.game_in_progress,
            'lights': self.rgb_to_hex()
        })

    def next_turn(self):
        self.current_player = self.get_next_player()
        print(f'current player set to: {self.current_player}')
        self.lights_off()
        self.update_lights(
            list(range(self.player_lights[self.current_player][0], self.player_lights[self.current_player][1])),
            (0,255,0))

    def lights_off(self) :
        self.update_all_lights()

    def lights_per_player(self, rgb=(0,0,0), delay=2):
        self.update_all_lights((0,255,0))

    # Light up sequentially as a train, cycle through colors
    def lights_on_sequential_rgb(self, delay=.02, num_cycles=1, colors = [(255,0,0),(0,255,0),(0,0,255)]):
        for _ in range(num_cycles):
            for color in colors:
                for light in self.lights:
                    light['r'] = color[0]
                    light['g'] = color[1]
                    light['b'] = color[2]
                    self.push_lights()
                    time.sleep(delay)

    # Light up one at a time sequentially
    def lights_on_sequential(self, num_loops = 1, rgb=(255,0,0), delay=0.02):
        orig_lights = copy.deepcopy(self.lights)
        for _ in range(num_loops):
            for i in range(len(self.lights)):
                self.lights[i]['r'] = rgb[0]
                self.lights[i]['g'] = rgb[1]
                self.lights[i]['b'] = rgb[2]
                self.lights[i-1]['r'] = 0
                self.lights[i-1]['g'] = 0
                self.lights[i-1]['b'] = 0
                self.push_lights()
                time.sleep(delay)
        self.lights = orig_lights
        self.push_lights()

    # Blink all lights together
    def blink_lights(self, num_blinks = 5, delay=0.4, color=(255,0,0)):
        orig_lights = copy.deepcopy(self.lights)
        for _ in range(num_blinks):
            self.lights_off()
            for light in self.lights:
                light['r'] = color[0]
                light['g'] = color[1]
                light['b'] = color[2]
            time.sleep(delay)
            self.push_lights()
            time.sleep(delay)
        self.lights = orig_lights
        self.push_lights()

    # Set all lights to random colors
    def lights_random(self) :
        for light in self.lights:
            light['r'] = random.randint(0,255)
            light['g'] = random.randint(0,255)
            light['b'] = random.randint(0,255)
        self.push_lights()