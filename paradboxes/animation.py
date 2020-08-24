"""
Module DocString
"""

import RPi.GPIO as GPIO
import time
import random
from color import ColorChooser


class Blink:
    """
    DocString
    """

    def __init__(self, pins, rgb=[255, 0, 0], interval=0.1, sequence=None):
        self.pins = pins
        self.red, self.green, self.blue = ColorChooser(rgb).get_rpi_colors()
        self.interval = interval
        sequence_check(sequence)

    def sequence_check(self, sequence):
        if(sequence != None):
            self.sequence = sequence

    def __repr__(self):
        return "Blink the LED Strip @ pins: {}, {}, {}".format(self.pins[0], self.pins[1], self.pins[2])

    def __str__(self):
        return "Blink an LED Strip with {}s between blinks.".format(self.interval)


class SoftBlink(Blink):
    """
    DocString
    """

    def __init__(self, pins, rgb, interval=0.1, sequence=None):
        pass

class SoftRandomBlink(Blink):
    """
    DocString
    """

    def __init__(self, pins, interval=0.1, seed=None):
        pass

class RandomBlink(Blink):
    """
    DocString
    """

    def __init__(self, pins, interval=0.1, seed=None):
        pass
