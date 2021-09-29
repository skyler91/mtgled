import json
import random
import asyncio
from lightcontroller import LightController
from webserver import WebService

from threading import Thread
import time
import zmq

COMMAND_TOPIC = 'command'
LIGHTS_TOPIC = 'update_lights'

context = zmq.Context()
# pub_socket = context.socket(zmq.PUB)
# pub_socket.bind('inproc://#1')
sub_socket = context.socket(zmq.SUB)
sub_socket.setsockopt(zmq.SUBSCRIBE, LIGHTS_TOPIC.encode())
sub_socket.connect('inproc://#1')

global_lights = []
players = [1, 2, 3, 6]
current_player = 0
player_lights = {}

def update_lights():
    pass
    #pub_socket.send_string(f'{LIGHTS_TOPIC} {json.dumps(global_lights)}')



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

def get_next_player() :
    global current_player
    global players

    if (current_player == 0) :
        return players[0]

    next_player_index = players.index(current_player) + 1
    if next_player_index >= len(players):
        next_player_index = 0
    return players[next_player_index]


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

def next_player_subscriber() :
    asyncio.set_event_loop(asyncio.new_event_loop())
    while (True) :
        event = player_sub_socket.recv().decode('utf-8')



def send_to_websocket(message):
    for client in clients:
        # print('writing message to client')
        client.write_message(message)
        # print('wrote message to client')

def main():
    # lights_thread = Thread(target = lights_random, args=[0.1])
    # lights_thread = Thread(target = lights_on_sequential, args=[(255,0,0)])
    # lights_thread = Thread(target = lights_on_sequential_rgb)
    # lights_thread = Thread(target = blink_lights)
    # lights_thread = Thread(target = lights_per_player)
    lights = []

    light_controller = LightController(context, lights)
    webserver = WebService(context, lights)

    #queue_listener_thread = Thread(target = event_subscriber)

    light_controller.start()
    webserver.start()
    #queue_listener_thread.start()

if __name__ == "__main__" :
    main()
