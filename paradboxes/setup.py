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


    def __init__(self, int_pin, motion_pin, led_address, led_channels):
        logging.basicConfig(format="%(message)s %(asctime)s", datefmt=" ---[%m/%d/%y %I:%M:%S %p]", filename="log.log", level=logging.INFO)
        logging.info("Created Board Object")
        self.int_pin = int_pin
        self.led_address = led_address
        self.led_channels = led_channels
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
        self.red_pwm = PWM(address=self.led_address)
        self.green_pwm = PWM(address=self.led_address)
        self.blue_pwm = PWM(address=self.led_address)
        self.red_pwm.setup()
        self.green_pwm.setup()
        self.blue_pwm.setup()
        self.red_pwm.frequency(150)
        self.green_pwm.frequency(150)
        self.blue_pwm.frequency(150)
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



#!/usr/bin/python
'''
**********************************************************************
* Filename    : PCA9685.py
* Description : A driver module for PCA9685
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Version     : v2.0.0
**********************************************************************

This class is not my work. All credit goes to SunFounder and Cavon for creating
this class. Thank you for making this open source
'''

import smbus
import time
import math

class PWM(object):
    """A PWM control class for PCA9685."""
    _MODE1              = 0x00
    _MODE2              = 0x01
    _SUBADR1            = 0x02
    _SUBADR2            = 0x03
    _SUBADR3            = 0x04
    _PRESCALE           = 0xFE
    _LED0_ON_L          = 0x06
    _LED0_ON_H          = 0x07
    _LED0_OFF_L         = 0x08
    _LED0_OFF_H         = 0x09
    _ALL_LED_ON_L       = 0xFA
    _ALL_LED_ON_H       = 0xFB
    _ALL_LED_OFF_L      = 0xFC
    _ALL_LED_OFF_H      = 0xFD

    _RESTART            = 0x80
    _SLEEP              = 0x10
    _ALLCALL            = 0x01
    _INVRT              = 0x10
    _OUTDRV             = 0x04


    RPI_REVISION_0 = ["900092"]
    RPI_REVISION_1_MODULE_B  = ["Beta", "0002", "0003", "0004", "0005", "0006", "000d", "000e", "000f"]
    RPI_REVISION_1_MODULE_A  = ["0007", "0008", "0009",]
    RPI_REVISION_1_MODULE_BP = ["0010", "0013"]
    RPI_REVISION_1_MODULE_AP = ["0012"]
    RPI_REVISION_2_MODULE_B  = ["a01041", "a21041"]
    RPI_REVISION_3_MODULE_B  = ["a02082", "a22082", "a32082"]
    RPI_REVISION_3_MODULE_BP = ["a020d3"]
    RPI_REVISION_3_MODULE_AP = ["9020e0", "9000c1"]

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "PCA9685.py":'

    def _get_bus_number(self):
        pi_revision = self._get_pi_revision()
        if   pi_revision == '0':
            return 0
        elif pi_revision == '1 Module B':
            return 0
        elif pi_revision == '1 Module A':
            return 0
        elif pi_revision == '1 Module B+':
            return 1
        elif pi_revision == '1 Module A+':
            return 0
        elif pi_revision == '2 Module B':
            return 1
        elif pi_revision == '3 Module B':
            return 1
        elif pi_revision == '3 Module B+':
            return 1
        elif pi_revision == '3 Module A+':
            return 1

    def _get_pi_revision(self):
        "Gets the version number of the Raspberry Pi board"
        # Courtesy quick2wire-python-api
        # https://github.com/quick2wire/quick2wire-python-api
        # Updated revision info from: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line.startswith('Revision'):
                    if line[11:-1] in self.RPI_REVISION_0:
                        return '0'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_B:
                        return '1 Module B'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_A:
                        return '1 Module A'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_BP:
                        return '1 Module B+'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_AP:
                        return '1 Module A+'
                    elif line[11:-1] in self.RPI_REVISION_2_MODULE_B:
                        return '2 Module B'
                    elif line[11:-1] in self.RPI_REVISION_3_MODULE_B:
                        return '3 Module B'
                    elif line[11:-1] in self.RPI_REVISION_3_MODULE_BP:
                        return '3 Module B+'
                    elif line[11:-1] in self.RPI_REVISION_3_MODULE_AP:
                        return '3 Module A+'
                    else:
                        print("Error. Pi revision didn't recognize, module number: %s" % line[11:-1])
                        print('Exiting...')
                        quit()
        except Exception as e:
            f.close()
            print(e)
            print('Exiting...')
            quit()
        finally:
            f.close()

    def __init__(self, bus_number=None, address=0x40):
        self.address = address
        if bus_number == None:
            self.bus_number = self._get_bus_number()
        else:
            self.bus_number = bus_number
        self.bus = smbus.SMBus(self.bus_number)

    def _debug_(self,message):
        if self._DEBUG:
            print(self._DEBUG_INFO,message)


    def setup(self):
        '''Init the class with bus_number and address'''
        self._debug_('Reseting PCA9685 MODE1 (without SLEEP) and MODE2')
        self.write_all_value(0, 0)
        self._write_byte_data(self._MODE2, self._OUTDRV)
        self._write_byte_data(self._MODE1, self._ALLCALL)
        time.sleep(0.005)

        mode1 = self._read_byte_data(self._MODE1)
        mode1 = mode1 & ~self._SLEEP
        self._write_byte_data(self._MODE1, mode1)
        time.sleep(0.005)
        self._frequency = 60

    def _write_byte_data(self, reg, value):
        '''Write data to I2C with self.address'''
        self._debug_('Writing value %2X to %2X' % (value, reg))
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception as i:
            print(i)
            self._check_i2c()

    def _read_byte_data(self, reg):
        '''Read data from I2C with self.address'''
        self._debug_('Reading value from %2X' % reg)
        try:
            results = self.bus.read_byte_data(self.address, reg)
            return results
        except Exception as i:
            print(i)
            self._check_i2c()

    def _check_i2c(self):
        import commands
        bus_number = self._get_bus_number()
        print("\nYour Pi Rivision is: %s" % self._get_pi_revision())
        print("I2C bus number is: %s" % bus_number)
        print("Checking I2C device:")
        cmd = "ls /dev/i2c-%d" % bus_number
        output = commands.getoutput(cmd)
        print('Commands "%s" output:' % cmd)
        print(output)
        if '/dev/i2c-%d' % bus_number in output.split(' '):
            print("I2C device setup OK")
        else:
            print("Seems like I2C have not been set, Use 'sudo raspi-config' to set I2C")
        cmd = "i2cdetect -y %s" % self.bus_number
        output = commands.getoutput(cmd)
        print("Your PCA9685 address is set to 0x%02X" % self.address)
        print("i2cdetect output:")
        print(output)
        outputs = output.split('\n')[1:]
        addresses = []
        for tmp_addresses in outputs:
            tmp_addresses = tmp_addresses.split(':')[1]
            tmp_addresses = tmp_addresses.strip().split(' ')
            for address in tmp_addresses:
                if address != '--':
                    addresses.append(address)
        print("Conneceted i2c device:")
        if addresses == []:
            print("None")
        else:
            for address in addresses:
                print("  0x%s" % address)
        if "%02X" % self.address in addresses:
            print("Wierd, I2C device is connected, Try to run the program again, If problem stills, email this information to support@sunfounder.com")
        else:
            print("Device is missing.")
            print("Check the address or wiring of PCA9685 Server driver, or email this information to support@sunfounder.com")
        raise IOError('IO error')

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, freq):
        '''Set PWM frequency'''
        self._debug_('Set frequency to %d' % freq)
        self._frequency = freq
        prescale_value = 25000000.0
        prescale_value /= 4096.0
        prescale_value /= float(freq)
        prescale_value -= 1.0
        self._debug_('Setting PWM frequency to %d Hz' % freq)
        self._debug_('Estimated pre-scale: %d' % prescale_value)
        prescale = math.floor(prescale_value + 0.5)
        self._debug_('Final pre-scale: %d' % prescale)

        old_mode = self._read_byte_data(self._MODE1);
        new_mode = (old_mode & 0x7F) | 0x10
        self._write_byte_data(self._MODE1, new_mode)
        self._write_byte_data(self._PRESCALE, int(math.floor(prescale)))
        self._write_byte_data(self._MODE1, old_mode)
        time.sleep(0.005)
        self._write_byte_data(self._MODE1, old_mode | 0x80)

    def write(self, channel, on, off):
        '''Set on and off value on specific channel'''
        self._debug_('Set channel "%d" to value "%d"' % (channel, off))
        self._write_byte_data(self._LED0_ON_L+4*channel, on & 0xFF)
        self._write_byte_data(self._LED0_ON_H+4*channel, on >> 8)
        self._write_byte_data(self._LED0_OFF_L+4*channel, off & 0xFF)
        self._write_byte_data(self._LED0_OFF_H+4*channel, off >> 8)

    def write_all_value(self, on, off):
        '''Set on and off value on all channel'''
        self._debug_('Set all channel to value "%d"' % (off))
        self._write_byte_data(self._ALL_LED_ON_L, on & 0xFF)
        self._write_byte_data(self._ALL_LED_ON_H, on >> 8)
        self._write_byte_data(self._ALL_LED_OFF_L, off & 0xFF)
        self._write_byte_data(self._ALL_LED_OFF_H, off >> 8)

    def map(self, x, in_min, in_max, out_min, out_max):
        '''To map the value from arange to another'''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        '''Set if debug information shows'''
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print(self._DEBUG_INFO, "Set debug on")
        else:
            print(self._DEBUG_INFO, "Set debug off")
