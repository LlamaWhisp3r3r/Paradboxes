"""
Module DocString
"""

class ColorChooser():
    """
    DocString
    """

    def __init__(self, rgb):
        self.rgb = rgb
        self.convert_rgb_to_rpi()
        self.red, self.green, self.blue = self.seperate_colors(self.rpi)

    def __repr__(self):
        return "ColorChooser Object {}, red={}, green={}, blue={}".format(self, self.red, self.green, self.blue)

    def __str__(self):
        return "Color is: red={}, green={}, blue={}".format(self.red, self.green, self.blue)

    def convert_rgb_to_rpi(self):
        self.rpi = []
        for color in self.rgb:
            # RPi uses values 0-100 to determine the brightness of the r, g, or b
            # So to convert regular rgb values to rpi values we need to divide by 255
            converted_color = color / 255
            rpi.append(converted_color)


class Color():
    """
    DocString
    """

    RED = ColorChooser([255, 0, 0]).rpi
    GREEN = ColorChooser([0, 255, 0]).rpi
    BLACK = ColorChooser([0, 0, 0]).rpi
    WHITE = ColorChooser([255, 255, 255]).rpi
    BLUE = ColorChooser([0, 0, 255]).rpi
    CYAN = ColorChooser([0, 255, 255]).rpi
    MAGENTA = ColorChooser([255, 0, 255]).rpi
    SILVER = ColorChooser([192, 192, 192]).rpi
    GRAY = ColorChooser([128, 128, 128]).rpi
    MAROON = ColorChooser([128, 0, 0]).rpi
    OLIVE = ColorChooser([128, 128, 0]).rpi
    PURPLE = ColorChooser([128, 0, 128]).rpi
    TEAL = ColorChooser([0, 128, 128]).rpi
    NAVY = ColorChooser([0, 0, 128]).rpi
    TURQUOISE = ColorChooser([64, 224, 208]).rpi
