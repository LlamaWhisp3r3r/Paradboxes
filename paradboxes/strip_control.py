"""
Provide high level control of the led strip color scheme. Currently only provides you\
with one led strip color control class, blink.

Classes:

Blink(self, pins, rgb=None, interval=0.1, timeout=10, sequence=None, random_sequence=False, soft=False, random=False, chaos=False)
ColorChooser()
"""


from gpiozero import PWMLED
import time
import random


class Blink():
    """
    Blinks an led strip in many different ways. Given that there are many different ways this can blink there is\
    an importance order. The order is:
    sequence, random, chaos, regular
    If soft is combined with any of these except chaos & regular than it is more important then if it didn't have soft.\
    For example within sequence there is an importance order:
    (random_sequence, soft), (random_sequence), (soft), (regular)
    The random is as follows:
    (soft), (regular)


    :param pins : list of pins for the led strip to control. Should be arranged as [redPin, greenPin, bluePin]
    :param rgb : list of rgb value. Should be arranged as [red, green, blue]. Defaults to None
    :param interval : the interval of change between colors. This value can differ depending on the effects
    :param timeout : How many times the light sequence will go through a cycle before timing out
    :param sequence : a list of rgb values. Arrangement should be [[rgb], [rgb], [rgb], ...]
    :param random_sequence : determines if you want the sequence to be shuffled through randomly
    :param soft : makes the colors change smoothly
    :param random : force the strip to go through colors randomly
    :param chaos : random colors and random intervals. Soft can not be combined with this
    """


    def __init__(self, pins, rgb=None, interval=0.1, timeout=10, sequence=None, random_sequence=False, soft=False, random=False, chaos=False):
        self.pins = pins
        self.sequence = sequence
        self.rgb = rgb
        self.interval = interval
        self.timeout = timeout
        self.random_sequence = random_sequence
        self.soft = soft
        self.random = random
        self.seperate_pins()
        self.check_sequence_and_rgb_are_real()


    def check_sequence_and_rgb_are_real(self):
        if self.sequence == None and self.rgb == None and not chaos, and not random:
            raise SyntaxError("No parameter was provided for sequence, rgb, random, or chaos. Please provide a parameter for one of these values")


    def seperate_pins(self):
        self.red_pin = self.pins[0]
        self.green_pin = self.pins[1]
        self.blue_pin = self.pins[2]


    def start(self):
        """
        Starts the correct function based on the parameters that were passed in
        """


        self.start_correct_function()


    def start_correct_function(self):
        if self.sequence_exist():
            function = self.get_correct_sequence_function()
            self.call_function_timeout_times(function)
        elif self.random and self.soft:
            self.current_random_rgb = self.get_random_rgb()
            self.call_function_timeout_times(self.random_soft_start)
        elif self.random:
            self.call_function_timeout_times(self.random_start)
        elif self.chaos:
            self.call_function_timeout_times(self.chaos_start)
        else:
            self.call_function_timeout_times(self.regular_start)


    def sequence_exist(self):
        if self.sequence != None:
            return True
        else:
            return False


    def get_correct_sequence_function(self):
        if self.random_sequence and self.soft:
            self.current_random_rgb = self.get_random_rgb_from_sequence_index()
            return self.go_through_sequence_randomly_softly
        elif self.random_sequence:
            return self.go_through_sequence_randomly
        elif self.soft:
            self.current_index = 0
            return self.go_through_sequence_softly
        else:
            return self.go_through_sequence


    def go_through_sequence_randomly_softly(self):
        current_random_rgb = self.current_random_rgb
        next_random_rgb = self.get_random_rgb_from_sequence_index()
        self.go_to_color(current_random_rgb.rgb, next_random_rgb.rgb)
        self.current_random_rgb = next_random_rgb


    def get_random_rgb_from_sequence_index(self):
        sequence_size = len(self.sequence) - 1
        random_index = random.randint(0, sequence_size)
        random_rgb = self.sequence[random_index]
        return random_rgb


    def go_to_color(self, current_rgb, next_rgb):
        current_red, current_green, current_blue = ColorChooser().set_color(current_rgb).seperate_rgb()
        next_red, next_green, next_blue = ColorChooser().set_color(next_rgb).seperate_rgb()
        self.increase_decrease(current_red, next_red, self.red_pin)
        self.increase_decrease(current_green, next_green, self.green_pin)
        self.increase_decrease(current_blue, next_blue, self.blue_pin)


    def increse_decrease(self, color, second_color, pin):
        if color > second_color:
            self.decrease_color_to_color(color, second_color)
        else:
            self.increase_color_to_color(color, second_color)


    def decrese_color_to_color(self, first_color, second_color, pin):
        for color in range(first_color, second_color-1, -1):
            pin.value = ColorChooser().convert_rgb_to_rpi(color)
            time.sleep(self.interval)


    def increase_color_to_color(self, first_color, second_color, pin):
        for color in range(first_color, second_color-1):
            pin.value = ColorChooser().convert_rgb_to_rpi(color)
            time.sleep(self.interval)


    def call_function_timeout_times(self, function):
        while self.timeout >= 0:
            function()
            self.timeout -= 1


    def go_through_sequence_randomly(self):
        random_rgb = self.get_random_rgb_from_sequence_index()
        self.change_strip_color(random_rgb)
        time.sleep(self.interval)


    def go_through_sequence_softly(self):
        current_rgb = self.sequence[self.current_index]

        if self.current_index == len(self.sequence)-2:
            self.current_index = 0
            next_rgb = self.sequence[self.current_index]
        else:
            next_rgb = self.sequence[self.current_index+1]

        self.got_to_color(current_rgb, next_rgb)
        self.current_index += 1


    def change_strip_color(self, rgb):
        self.red_pin.value = ColorChooser().convert_rgb_to_rpi(rgb[0])
        self.green_pin.value = ColorChooser().convert_rgb_to_rpi(rgb[1])
        self.blue_pin.value = ColorChooser().convert_rgb_to_rpi(rgb[2])


    def go_through_sequence(self):
        for rgb in self.sequence:
            self.change_strip_color(rgb)
            time.sleep(self.interval)


    def random_soft_start(self):
        current_random_rgb = self.current_random_rgb
        next_random_rgb = self.get_random_rgb()
        self.go_to_color(current_random_rgb, next_random_rgb)
        self.current_random_rgb = next_random_rgb


    def get_random_rgb(self):
        rgb = []
        rgb.append(random.randint(0, 255))
        rgb.append(random.randint(0, 255))
        rgb.append(random.randint(0, 255))
        return rgb


    def random_start(self):
        rgb = self.get_random_rgb()
        self.change_strip_color(rgb)
        time.sleep(self.interval)


    def regular_start(self):
        self.change_strip_color(self.rgb)
        time.sleep(self.interval)
        self.change_strip_color([0, 0, 0])
        time.sleep(self.interval)

    def chaos_start(self):
        interval = random.randint(0, 100)/100
        rgb = self.get_random_rgb()
        self.change_strip_color(rgb)
        time.sleep(interval)


    def __repr__(self):
        return "Blink the LED Strip @ pins: {}, {}, {}".format(self.pins[0], self.pins[1], self.pins[2])


    def __str__(self):
        return "Blink an LED Strip with {}s between blinks.".format(self.interval)


class ColorChooser():
    """
    Holder for colors in two types. rpi, a 0-1 value (mostly used in the gpiozero.PWMLED)\
    rgb, a 0-255 value.
    """


    def set_color(self, rgb):
        """
        Sets the color of the object to the parameter

        :param rgb : list of rgb values. Arranged as so [red, green, blue]
        """


        self.rgb = rgb
        self.rpi = []
        self.red, self.green, self.blue = self.get_converted_colors(self.rgb)


    def get_converted_colors(self, colors):
        red = self.convert_rgb_to_rpi(colors[0])
        green = self.convert_rgb_to_rpi(colors[1])
        blue = self.convert_rgb_to_rpi(colors[2])
        return red, green, blue


    def set_rpi(self):
        self.rpi.append(self.red)
        self.rpi.append(self.green)
        self.rpi.append(self.blue)


    def __repr__(self):
        return "ColorChooser Object {}, red={}, green={}, blue={}".format(self, self.red, self.green, self.blue)

    def __str__(self):
        return "Color is: red={}, green={}, blue={}".format(self.red, self.green, self.blue)

    def convert_rgb_to_rpi(self, color):
        """
        Converts the rgb value, the parameter, into a rpi value.

        :param color : rgb value to be converted
        """


        # RPi uses values 0-100 to determine the brightness of the r, g, or b
        # So to convert regular rgb values to rpi values we need to divide by 255
        converted_color = color / 255
        return converted_color


    def seperate_rpi(self):
        red = self.rpi[0]
        green = self.rpi[1]
        blue = self.rpi[2]
        return red, green , blue


    def seperate_rgb(self):
        red = self.rgb[0]
        green = self.rgb[1]
        blue = self.rgb[2]
        return red, green , blue
#
# class Color():
#     """
#     DocString
#     """
#
#     RED = ColorChooser().set_color([255, 0, 0]).rgb
#     GREEN = ColorChooser().set_color([0, 255, 0]).rgb
#     BLACK = ColorChooser().set_color([0, 0, 0]).rgb
#     WHITE = ColorChooser().set_color([255, 255, 255]).rgb
#     BLUE = ColorChooser().set_color([0, 0, 255]).rgb
#     CYAN = ColorChooser().set_color([0, 255, 255]).rgb
#     MAGENTA = ColorChooser().set_color([255, 0, 255]).rgb
#     SILVER = ColorChooser().set_color([192, 192, 192]).rgb
#     GRAY = ColorChooser().set_color([128, 128, 128]).rgb
#     MAROON = ColorChooser().set_color([128, 0, 0]).rgb
#     OLIVE = ColorChooser().set_color([128, 128, 0]).rgb
#     PURPLE = ColorChooser().set_color([128, 0, 128]).rgb
#     TEAL = ColorChooser().set_color([0, 128, 128]).rgb
#     NAVY = ColorChooser().set_color([0, 0, 128]).rgb
#     TURQUOISE = ColorChooser().set_color([64, 224, 208]).rgb
