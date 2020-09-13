"""
Module DocString
"""

from gpiozero import PWMLED
import time
import random
from color import ColorChooser


class Blink():
    """
    DocString
    """

    def __init__(self, pins, rgb=None, interval=0.1, timeout=10, sequence=None, random_sequence=False, soft=False, random=False):
        self.pins = pins
        self.sequence = sequence
        self.rgb = ColorChooser(rgb).rpi
        self.interval = interval
        self.timeout = timeout
        self.random_sequence = random_sequence
        self.soft = soft
        self.random = random
        self.seperate_pins()
        self.check_sequence_and_rgb_are_real()
        self.get_colors_if_not_none()

    def check_sequence_and_rgb_are_real(self):
        if self.sequence == None && self.rgb == None:
            raise SyntaxError("No parameter was provided for sequence or rgb.")

    def seperate_pins(self):
        self.red_pin = self.pins[0]
        self.green_pin = self.pins[1]
        self.blue_pin = self.pins[2]

    def start(self):
        self.start_correct_pattern(self)

    def start_correct_function(self):
        if self.sequence_exist():
            function = self.get_correct_sequence_function()
            self.call_function_timeout_times(function)
        elif self.random and self.soft:
            self.call_function_timeout_times()
        elif self.random:
            self.call_function_timeout_times()
        else:
            self.call_function_timeout_times(self.regular_start)

    def sequence_exist(self):
        if self.sequence != None:
            return False
        else:
            return True

    def get_correct_sequence_function(self):
        if self.random_sequence and self.soft:
            return self.go_through_sequence_randomly_softly
        elif self.random_sequence:
            return self.go_through_sequence_randomly
        else:
            return self.go_through_sequence

    def go_through_sequence_randomly_softly(self):
        pass

    def get_random_rgb_from_sequence_index(self):
        sequence_size = len(self.sequence) - 1
        random_index = random.randint(0, sequence_size)
        random_rgb = self.sequence[random_index]
        return random_rgb

    def call_function_timeout_times(self, function):
        while self.timeout >= 0:
            function()

    def go_through_sequence_randomly(self):
        random_rgb = self.get_random_rgb_from_sequence_index()
        self.change_strip_color(random_rgb)
        time.sleep(self.interval)

    def change_strip_color(self, rgb):
        self.red_pin.value = rgb[0]
        self.green_pin.value = rgb[1]
        self.blue_pin.value = rgb[2]

    def go_through_sequence(self):
        for rgb in self.sequence:
            change_strip_color(rgb)
            time.sleep(self.interval)

    def regular_start(self):
        self.change_strip_color(self.rgb)

    def __repr__(self):
        return "Blink the LED Strip @ pins: {}, {}, {}".format(self.pins[0], self.pins[1], self.pins[2])

    def __str__(self):
        return "Blink an LED Strip with {}s between blinks.".format(self.interval)
