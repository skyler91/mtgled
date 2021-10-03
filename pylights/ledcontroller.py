import board
import json
import neopixel
import os
import zmq
from lightcontroller import LED_UPDATE_TOPIC

# GPIO 18
LED_PIN = board.D18
LED_PUB_ADDRESS = 'localhost'
LED_PUB_PORT = 8757

class LedController:
    def __init__(self, num_lights, brightness):
        self.num_lights = num_lights
        self.brightness = brightness
        self.leds = neopixel.NeoPixel(LED_PIN, num_lights, brightness=brightness, auto_write=False)

    # Pushes an update to LEDS
    def update(self, leds):
        if len(leds) != self.num_lights :
            raise ValueError('LED number mismatch')

        for i in range(len(leds)):
            self.leds[i] = (leds[i]['r'], leds[i]['g'], leds[i]['b'])

        self.leds.show()

def led_sub_listener(controller):
    context = zmq.Context()
    led_sub_socket = context.socket(zmq.SUB)
    led_sub_socket.setsockopt(zmq.SUBSCRIBE, LED_UPDATE_TOPIC)
    led_sub_socket.connect(f"tcp://{os.environ.get('LED_PUB_ADDRESS') or LED_PUB_ADDRESS}:{os.environ.get('LED_PUB_PORT') or LED_PUB_PORT}")
    while True:
        message = led_sub_socket.recv_multipart()
        print(f'received message with {len(message)} parts')
        leds = json.loads(message[1].decode('utf-8'))
        print(f'updating LEDs: {leds}')
        controller.update(leds)

if __name__ == "__main__":
    led_controller = LedController(148, 0.5)
    led_sub_listener(led_controller)