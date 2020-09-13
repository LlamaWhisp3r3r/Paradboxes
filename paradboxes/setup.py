"""
Module DocString
"""

from gpiozero import *
import board
import digitalio
import busio
import adafruit_lis3dh
import adafruit_tcs34725

class InitializeBoard:

    def __init__(self, int_pin, motion_pin, led_pins):
        self.int_pin = int_pin
        self.led_pins = led_pins
        self.motion_pin = motion_pin
        self._initialize_components()

    def _initialize_components(self):
        self._initialize_i2c()
        self._initialize_led()
        self._initialize_motion()

    def _initialize_i2c(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        interupt_pin = digitalio.DigitalInOut(board.D6)
        self.accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=interupt_pin)
        self.color_sensor = adafruit_tcs34725.TCS34725(i2c)

    def _initialize_led(self):
        self.red_pwm = PWMLED(self.led_pins[0])
        self.green_pwm = PWMLED(self.led_pins[1])
        self.blue_pwm = PWMLED(self.led_pins[2])

    def _initialize_motion(self):
        self.motion_sensor = GPIODevice(self.motion_pin)
