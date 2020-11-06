"""
Provide high level control of the led strip color scheme. Currently only provides you\
with one led strip color control class, blink.

Classes:

Blink(self, pins, channels=[12, 8, 4], rgb=None, interval=0.1, timeout=10, sequence=None,
      interval_sequence=None, random_sequence=False, soft=False, random_flag=False, chaos=False, random_rgb_start=None)
ColorChooser(rgb)
"""

import logging
import time
import random


class Blink:
    """
    Blinks an led strip in many different ways. Given that there are many different ways this can blink there is
    an importance order. The order is:
    sequence, random, chaos, regular
    If soft is combined with any of these except chaos & regular than it is more important then if it didn't have soft.
    For example within sequence there is an importance order:
    (random_sequence, soft), (random_sequence), (soft), (regular)
    The random is as follows:
    (soft), (regular)


    :param pwm : pwm object
    :param channels : list of channels in the following order: [redChannel, blueChannel, greenChannel]
    :param rgb : list of rgb value. Should be arranged as [red, green, blue]. Defaults to None
    :param interval : the interval of change between colors. This value can differ depending on the effects
    :param timeout : How many times the light sequence will go through a cycle before timing out
    :param sequence : a list of rgb values. Arrangement should be [[rgb], [rgb], [rgb], ...]
    :param random_sequence : determines if you want the sequence to be shuffled through randomly
    :param soft : makes the colors change smoothly
    :param random_flag : force the strip to go through colors randomly
    :param chaos : random colors and random intervals. Soft can not be combined with this
    :param random_rgb_start : starting point for random colors. Defaults to None
    """

    def __init__(self, pwm, channels=[12, 8, 4], rgb=None, interval=0.1, timeout=10, sequence=None,
                 interval_sequence=None, random_sequence=False, soft=False, random_flag=False, chaos=False,
                 random_rgb_start=None):

        # Configure logging
        if channels is None:
            channels = [12, 8, 4]
        logging.basicConfig(format="%(message)s %(asctime)s", datefmt=" ---[%m/%d/%y %I:%M:%S %p]", filename="log.log",
                            level=logging.INFO)
        logging.info("Created Blink Object")

        self.pwm = pwm
        self.channels = channels
        self.sequence = sequence
        self.rgb = rgb
        self.interval = interval
        self.timeout = timeout
        self.random_sequence = random_sequence
        self.interval_sequence = interval_sequence
        self.soft = soft
        self.random = random_flag
        self.chaos = chaos
        self.random_rgb_start = random_rgb_start
        self.current_color = []
        self.__separate_channels()
        self.__check_sequence_and_rgb_are_real()

    def __check_sequence_and_rgb_are_real(self):
        if self.sequence is None and self.rgb is None and not self.chaos and not self.random:
            raise SyntaxError("No parameter was provided for sequence, rgb, random_flag, or chaos. Please provide a "
                              "parameter for one of these values")

    def __separate_channels(self):
        self.red_channel = self.channels[0]
        self.green_channel = self.channels[1]
        self.blue_channel = self.channels[2]

    def start(self):
        """
        Starts the correct function based on the parameters that were passed in
        """

        logging.info("Started an LED Strip Blink Animation")
        self.__start_correct_function()

    def __start_correct_function(self):

        if self.__sequence_exist():
            function = self.__get_correct_sequence_function
            self.__call_function_timeout_times(function)
        elif self.random and self.soft:
            if self.random_rgb_start is not None:
                self.current_random_rgb = self.random_rgb_start
            else:
                self.current_random_rgb = self.__get_random_rgb()
            self.__call_function_timeout_times(self.__random_soft_start)
        elif self.random:
            if self.interval_sequence is not None:
                self.current_interval_index = -1
            self.__call_function_timeout_times(self.__random_start)
        elif self.chaos:
            self.__call_function_timeout_times(self.__chaos_start)
        else:
            self.__call_function_timeout_times(self.__regular_start)

    def __sequence_exist(self):

        if self.sequence is not None:
            return True
        else:
            return False

    def __get_correct_sequence_function(self):

        if self.random_sequence and self.soft:
            self.current_random_rgb = self.__get_random_rgb_from_sequence_index()
            return self.__go_through_sequence_randomly_softly
        elif self.random_sequence:
            return self.__go_through_sequence_randomly
        elif self.soft:
            self.current_index = 0
            return self.__go_through_sequence_softly
        else:
            return self.__go_through_sequence

    def __go_through_sequence_randomly_softly(self):

        logging.info("Starting random_flag soft sequence LED Strip Animation")
        current_random_rgb = self.current_random_rgb
        next_random_rgb = self.__get_random_rgb_from_sequence_index()
        self.go_to_color(current_random_rgb.rgb, next_random_rgb.rgb)
        self.current_random_rgb = next_random_rgb

    def __get_random_rgb_from_sequence_index(self):

        sequence_size = len(self.sequence) - 1
        random_index = random.randint(0, sequence_size)
        random_rgb = self.sequence[random_index]
        return random_rgb

    def go_to_color(self, current_rgb, next_rgb):
        """
        Go from current_rgb to next_rgb one rgb value at a time. Going through the following values: red, green, blue

        :param current_rgb : starting rgb value
        :param next_rgb : ending rgb value
        """

        color_one = ColorChooser(current_rgb)
        color_two = ColorChooser(next_rgb)
        current_red, current_green, current_blue = color_one.separate_rgb()
        next_red, next_green, next_blue = color_two.separate_rgb()

        logging.info("Changing LED Strip color from {} to {}".format(current_rgb, next_rgb))
        self.__increase_decrease(current_red, next_red, self.red_channel)
        self.__increase_decrease(current_green, next_green, self.green_channel)
        self.__increase_decrease(current_blue, next_blue, self.blue_channel)
        logging.info("Changed LED Strip color from {} to {}".format(current_rgb, next_rgb))

        self.current_color = next_rgb

    def __increase_decrease(self, color, second_color, channel):

        if color > second_color:
            self.__decrease_color_to_color(color, second_color, channel)
        else:
            self.__increase_color_to_color(color, second_color, channel)

    def __decrease_color_to_color(self, first_color, second_color, channel):

        for color in range(first_color, second_color - 1, -1):
            self.change_channel_color(color, channel)
            time.sleep(self.interval)

    def __increase_color_to_color(self, first_color, second_color, channel):

        for color in range(first_color, second_color - 1):
            self.change_channel_color(color, channel)
            time.sleep(self.interval)

    def change_channel_color(self, color, channel):
        """
        Change a single channel's color to specified color

        :param color : rgb color value
        :param channel : channel of the
        """

        value = ColorChooser([0, 0, 0]).convert_rgb_to_rpi(color)
        self.pwm.write(channel, 0, value)

    def __call_function_timeout_times(self, function):
        while self.timeout >= 0:
            function()
            self.timeout -= 1

    def __go_through_sequence_randomly(self):
        logging.info("Starting random_flag sequence LED Strip Animation")
        random_rgb = self.__get_random_rgb_from_sequence_index()
        self.change_strip_color(random_rgb)
        time.sleep(self.interval)

    def __go_through_sequence_softly(self):
        logging.info("Starting softly sequence LED Strip Animation")
        current_rgb = self.sequence[self.current_index]

        if self.current_index == len(self.sequence) - 2:
            self.current_index = 0
            next_rgb = self.sequence[self.current_index]
        else:
            next_rgb = self.sequence[self.current_index + 1]

        self.go_to_color(current_rgb, next_rgb)
        self.current_index += 1

    def change_strip_color(self, rgb):
        """
        Change the strip color to the specified strip value

        :param rgb : rgb value in a list. [red, green, blue]
        """

        logging.info("Changing LED Strip color to {}".format(rgb))

        self.current_color = rgb
        red_off = ColorChooser([0, 0, 0]).convert_rgb_to_rpi(rgb[0])
        green_off = ColorChooser([0, 0, 0]).convert_rgb_to_rpi(rgb[1])
        blue_off = ColorChooser([0, 0, 0]).convert_rgb_to_rpi(rgb[2])

        self.pwm.write(self.red_channel, 0, red_off)
        self.pwm.write(self.green_channel, 0, green_off)
        self.pwm.write(self.blue_channel, 0, blue_off)

    def __go_through_sequence(self):
        logging.info("Starting regular sequence LED Strip Animation")
        for rgb in self.sequence:
            self.change_strip_color(rgb)
            time.sleep(self.interval)

    def __random_soft_start(self):
        logging.info("Starting random_flag soft LED Strip Animation")
        current_random_rgb = self.current_random_rgb
        next_random_rgb = self.__get_random_rgb()
        self.go_to_color(current_random_rgb, next_random_rgb)
        self.current_random_rgb = next_random_rgb

    def __get_random_rgb(self):
        rgb = list()
        rgb.append(random.randint(0, 255))
        rgb.append(random.randint(0, 255))
        rgb.append(random.randint(0, 255))
        return rgb

    def __random_start(self):
        logging.info("Starting random_flag LED Strip Animation")
        rgb = self.__get_random_rgb()
        self.change_strip_color(rgb)
        if self.interval_sequence is not None:
            self.current_interval_index += 1
            self.interval = self.interval_sequence[self.current_interval_index]
        time.sleep(0.1)
        self.change_strip_color([255, 255, 255])
        time.sleep(self.interval)

    def __regular_start(self):
        logging.info("Starting regular LED Strip Animation")
        self.change_strip_color(self.rgb)
        time.sleep(self.interval)
        self.change_strip_color([0, 0, 0])
        time.sleep(self.interval)

    def __chaos_start(self):
        logging.info("Starting chaos LED Strip Animation")
        interval = random.randint(0, 100) / 100
        rgb = self.__get_random_rgb()
        self.change_strip_color(rgb)
        time.sleep(interval)

    def __repr__(self):
        return "Blink the LED Strip @ channel: {}, {}, {}".format(self.channels[0], self.channels[1], self.channels[2])

    def __str__(self):
        return "Blink an LED Strip with {}s between blinks.".format(self.interval)


class ColorChooser:
    """
    Holder for colors in two types. Driver, 0-4095, and rgb, a 0-255 value.
    """

    def __init__(self, rgb):
        self.rgb = rgb
        self.rpi = []
        self.red, self.green, self.blue = self.get_converted_colors(self.rgb)

    def set_color(self, rgb):
        """
        Sets the color of the object to the parameter

        :param rgb : list of rgb values. Arranged as so [red, green, blue]
        """

        self.rgb = rgb
        self.red, self.green, self.blue = self.get_converted_colors(self.rgb)

    def get_converted_colors(self, colors):
        red = self.convert_rgb_to_rpi(colors[0])
        green = self.convert_rgb_to_rpi(colors[1])
        blue = self.convert_rgb_to_rpi(colors[2])
        return red, green, blue

    def __repr__(self):
        return "ColorChooser Object {}, red={}, green={}, blue={}".format(self, self.red, self.green, self.blue)

    def __str__(self):
        return "Color is: red={}, green={}, blue={}".format(self.red, self.green, self.blue)

    def convert_rgb_to_rpi(self, color):
        """
        Converts the rgb value, the parameter, into a driver value (0-4095)

        :param color : rgb value to be converted
        """

        # Driver uses values 0-4095 to determine the brightness of the r, g, or b
        # So to convert regular rgb values to the drivers values we need to divide by 255
        # Then multiple it by 4095 so that the pwm pin can read the value
        # Then do 4095 minus the value, and round. (Driver doesn't take floats)
        off_color = int(4095 - ((color / 255) * 4095))
        return off_color

    def separate_rgb(self):
        red = self.rgb[0]
        green = self.rgb[1]
        blue = self.rgb[2]
        return red, green, blue
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
