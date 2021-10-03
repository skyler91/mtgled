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

        for i in range(len(leds)):
            self.leds[i] = (leds[i]['r'], leds[i]['g'], leds[i]['b'])

        self.leds.show()