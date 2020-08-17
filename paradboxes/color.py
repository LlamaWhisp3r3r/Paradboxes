"""
Module DocString
"""

class ColorChooser():
    """
    DocString
    """

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return "ColorChooser Object {}, red={}, green={}, blue={}".format(self, self.red, self.green, self.blue)

    def __str__(self):
        return "Color is: red={}, green={}, blue={}".format(self.red, self.green, self.blue)

class Color():
    """
    DocString
    """
    
    RED = ColorChooser(255, 0, 0)
    GREEN = ColorChooser(0, 255, 0)
    BLACK = ColorChooser(0, 0, 0)
    WHITE = ColorChooser(255, 255, 255)
    BLUE = ColorChooser(0, 0, 255)
    CYAN = ColorChooser(0, 255, 255)
    MAGENTA = ColorChooser(255, 0, 255)
    SILVER = ColorChooser(192, 192, 192)
    GRAY = ColorChooser(128, 128, 128)
    MAROON = ColorChooser(128, 0, 0)
    OLIVE = ColorChooser(128, 128, 0)
    PURPLE = ColorChooser(128, 0, 128)
    TEAL = ColorChooser(0, 128, 128)
    NAVY = ColorChooser(0, 0, 128)
    TURQUOISE = ColorChooser(64, 224, 208)
