"""
Module DocString
"""

from gpiozero import PWMLED
import time
import random
from color import ColorChooser


class Blink(LEDSetup):
    """
    DocString
    """

    def __init__(self, pins, rgb=None, interval=0.1, timeout=None sequence=None, random_sequence=False):
        self.pins = pins
        self.sequence = sequence
        self.rgb = rgb
        self.interval = interval
        self.check_sequence_and_rgb_are_real()

    def check_sequence_and_rgb_are_real(self):
        if self.sequence == None && self.rgb == None:
            raise SyntaxError("No value was provided to sequence or rgb.")

    def get_colors_if_not_none(self):
        if self.rgb != None:
            self.red, self.green, self.blue = ColorChooser(rgb).get_rpi_colors()

    def sequence_exist(self):
        if self.sequence != None:
            return False
        else:
            return True

    def start(self):
        if(self.sequence_exist()):
            self.start_sequence()
        else:
            pass

    def start_sequence(self):
        pass

    def go_through_sequence(self):
        pass

    def change_strip_color(self, rgb):
        pass

    def set_duty_cycle(self, value):
        pass


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
