#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse

from dotenv import dotenv_values
config = dotenv_values("/home/pi/RasQberry/rasqberry_environment.env")

LED_COUNT = int(config["LED_COUNT"])
LED_PIN = int(config["LED_PIN"])
LED_FREQ_HZ = int(config["LED_FREQ_HZ"])  # LED signal frequency in hertz (usually 800khz)
LED_DMA = int(config["LED_DMA"])          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = int(config["LED_BRIGHTNESS"])  # Set to 0 for darkest and 255 for brightest
LED_INVERT = bool(config["LED_INVERT"]=="true" or config["LED_INVERT"]=="True")    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = int(config["LED_CHANNEL"])       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=150):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 10.0)


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return Color(r, g, b)

def rainbowCycle(strip, wait_ms=10, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(255 * iterations):
        for i in range(strip.numPixels()):
        #    print('j=',j,'i=',i)
        #    print(i, wheel(
        #       (int(i * 256 / strip.numPixels()) + j) & 255))
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the LEDs on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            rainbowCycle(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
