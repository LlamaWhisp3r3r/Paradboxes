"""
Provide nessicary board setup for raspberry pi.

Classes:

InitializeBoard(int_pin, motion_pin, led_pins)
"""


from gpiozero import *
import board
import digitalio
import busio
import adafruit_lis3dh
import adafruit_tcs34725
import logging


class InitializeBoard:
    """
    Set board components up for raspberry pi.

    :param int_pin : interupt pin number for accelerometer
    :param motion_pin : data pin number for motion sensor
    :param led_pins : lsit of pin numbers for led pins. Order should be [redPin, greenPin, bluePin]
    """


    def __init__(self, int_pin, motion_pin, led_pins):
        logging.basicConfig(format="%(message)s %(asctime)s", datefmt=" ---[%m/%d/%y %I:%M:%S %p]", filename="log.log", level=logging.INFO)
        logging.info("Created Board Object")
        self.int_pin = int_pin
        self.led_pins = led_pins
        self.motion_pin = motion_pin
        self.i2c = busio.I2C(board.SCL, board.SDA)


    def _initialize_components(self):
        self._initialize_i2c()
        self._initialize_led()
        self._initialize_motion()


    def _initialize_i2c(self):
        self._initialize_color_sensor()
        self._initialize_accelerometer()
        logging.info("I2C buses initialized")

    def _initialize_accelerometer(self):
        interupt_pin = digitalio.DigitalInOut(self.int_pin)
        self.accelerometer = adafruit_lis3dh.LIS3DH_I2C(self.i2c, int1=interupt_pin)

    def _initialize_color_sensor(self):
        self.color_sensor = adafruit_tcs34725.TCS34725(self.i2c)


    def _initialize_led(self):
        self.red_pwm = PWMLED(self.led_pins[0])
        self.green_pwm = PWMLED(self.led_pins[1])
        self.blue_pwm = PWMLED(self.led_pins[2])
        logging.info("LED Pins initialized")


    def _initialize_motion(self):
        self.motion_sensor = GPIODevice(self.motion_pin)
        logging.info("Motion Sensor intialized")


    def get_led_pins(self):
        """
        Return list of led pins in the form of a gpiozero.PWMLED object

        :return pwms : list of led pwms
        :rtype pwms : gpiozero.PWNLED
        """


        pwms = []
        pwms.append(self.red_pwm)
        pwms.append(self.green_pwm)
        pwms.append(self.blue_pwm)
        return pwms

    def close_all(self):
        self.red_pwm.close()
        self.green_pwm.close()
        self.blue_pwm.close()
        self.motion_sensor.close()
        logging.info("Closed all the pins")
