from gpiozero import *
import board
import digitalio
import busio
import adafruit_lis3dh
import adafruit_tcs34725


class ActionEvents:

    def __init__(self):
        pass

    def accelerometer_event(self, accelerometer, callback, tap=True):
        self.accelerometer = accelerometer
        self.accel_callback = callback
        if(Tap == True):
            self.wait_for_tap()
        else:
            print("Tap not set")

    def wait_for_tap(self):
        while True:
            if accelerometer.tapped:
                self.run_callback(self.accel_callback)

    def motion_event(self, data_pin, callback):
        self.data_pin = data_pin
        self.motion_callback = callback
        self.wait_for_motion()

    def wait_for_motion(self):
        while pin_equals_zero(self.data_pin):
            pass
        self.run_callback(self.motion_callback)

    def pin_equals_one(self, pin_value):
        if self.pin_value() == 0:
            return True
        else:
            return False

    def pin_value(self):
        return self.data_pin.value

    def run_callback(self, callback):
        callback()
