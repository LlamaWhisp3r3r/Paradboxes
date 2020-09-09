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
            # So to convert regular rgb values to rpi values we need to divide by 2.55
            converted_color = color / 2.55
            rpi.append(color)

    def seperate_colors(self, list):
        return list[0], list[1], list[2]

    def get_rpi_colors(self):
        return seperate_colors(self.rpi)

    def get_rgb_colors(self):
        return seperate_colors(self.rgb)


class Color():
    """
    DocString
    """

    RED = ColorChooser([255, 0, 0])
    GREEN = ColorChooser([0, 255, 0])
    BLACK = ColorChooser([0, 0, 0])
    WHITE = ColorChooser([255, 255, 255])
    BLUE = ColorChooser([0, 0, 255])
    CYAN = ColorChooser([0, 255, 255])
    MAGENTA = ColorChooser([255, 0, 255])
    SILVER = ColorChooser([192, 192, 192])
    GRAY = ColorChooser([128, 128, 128])
    MAROON = ColorChooser([128, 0, 0])
    OLIVE = ColorChooser([128, 128, 0])
    PURPLE = ColorChooser([128, 0, 128])
    TEAL = ColorChooser([0, 128, 128])
    NAVY = ColorChooser([0, 0, 128])
    TURQUOISE = ColorChooser([64, 224, 208])
