import board
import neopixel

# GPIO 18
LED_PIN = board.D18

class LedController:
    def __init__(self, num_lights, brightness):
        self.num_lights = num_lights
        self.brightness = brightness
        self.leds = neopixel.NeoPixel(LED_PIN, num_lights, brightness=brightness, auto_write=False)

    # Pushes an update to LEDS
    def update(self, leds):
        if len(leds) != self.num_lights :
            raise ValueError('LED number mismatch')

        pixels = []
        for l in leds:
            pixels.append((l['r'], l['g'], l['b']))

        pixels.show()