"""
Module DocString
"""

class ColorChooser():
    """
    DocString
    """

    def __init__(self):
        pass

    def set_color(self, rgb):
        self.rgb = rgb
        self.rpi = []
        self.red, self.green, self.blue = self.get_converted_colors(self.rgb)

    def get_converted_colors(self, colors):
        red = convert_rgb_to_rpi(colors[0])
        green = convert_rgb_to_rpi(colors[1])
        blue = convert_rgb_to_rpi(colors[2])
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

class Color():
    """
    DocString
    """

    RED = ColorChooser([255, 0, 0]).rgb
    GREEN = ColorChooser([0, 255, 0]).rgb
    BLACK = ColorChooser([0, 0, 0]).rgb
    WHITE = ColorChooser([255, 255, 255]).rgb
    BLUE = ColorChooser([0, 0, 255]).rgb
    CYAN = ColorChooser([0, 255, 255]).rgb
    MAGENTA = ColorChooser([255, 0, 255]).rgb
    SILVER = ColorChooser([192, 192, 192]).rgb
    GRAY = ColorChooser([128, 128, 128]).rgb
    MAROON = ColorChooser([128, 0, 0]).rgb
    OLIVE = ColorChooser([128, 128, 0]).rgb
    PURPLE = ColorChooser([128, 0, 128]).rgb
    TEAL = ColorChooser([0, 128, 128]).rgb
    NAVY = ColorChooser([0, 0, 128]).rgb
    TURQUOISE = ColorChooser([64, 224, 208]).rgb
