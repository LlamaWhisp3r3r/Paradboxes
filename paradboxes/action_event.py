"""
Only stores class Action Events
"""


from gpiozero import *
import board
import digitalio
import busio
import adafruit_lis3dh
import adafruit_tcs34725
import time
import logging


class ActionEvents:
    """
    All the action events for all the sensors.

    Functions:

    accelerometer_event(self, accelerometer, callback, sensitivity=60, tap=True, double_tap=False, multiple_tap=False, timeout=600)
    motion_event(self, data_pin, callback)
    """

    def __init__(self):
        logging.basicConfig(format="%(message)s %(asctime)s", datefmt=" ---[%m/%d/%y %I:%M:%S %p]", filename="log.log", level=logging.INFO)
        logging.info("ActionEvent Object created")



    def accelerometer_event(self, accelerometer, callback, sensitivity=60, tap=True, double_tap=False, multiple_tap=False, timeout=600):
        """
        Call back a given function when the specfied action event happens on the accelerometer.\
        You can set multiple action events to be true, but not all the action events \
        will be executed. The order of importance is (Most to Least important):
        Tap, Double Tap, Multiple Tap

        :param accelerometer : A adafruit circuit-python accelerometer object
        :param callback : callable function
        :param sensitivity : sensitivity of the accelerometer. Default is 60, can range from 0 - 100
        :param tap : a single tap of the accelerometer. Action event
        :param double_tap : a double tap of the accelerometer. Action event
        :param multiple_tap : records the sequence of taps in a 10 second time period. Action event
        :param timeout : the amount of time that it takes for the wait to timeout. Defaults to 600 seconds
        """


        logging.info("Accelerometer Event created")
        self.accelerometer = accelerometer
        self.accel_callback = callback
        self.timeout = timeout
        # Get the type of action that you want to wait for
        if Tap:
            self.accelerometer.set_tap(1, sensitivity)
            self.wait_for_tap()
        elif double_tap:
            self.accelerometer.set_tap(2, sensitivity)
            self.wait_for_tap()
        elif multiple_tap:
            self.accelerometer.set_tap(1, sensitivity)
            self.wait_for_tap_sequence()
        else:
            raise SyntaxError("No action event was set.")


    def wait_for_tap(self):
        """
        Wait for either double or single tap to execute then call the accelerometer callback
        """


        tracker = 0
        while tracker <= timeout:
            time_mark = time.time()
            if self.accelerometer.tapped:
                logging.info("Single Tap Detected")
                self.run_callback(self.accel_callback)
            tracker = time_mark - time.time()
        logging.info("Waiting for tap timeout")
        self.run_callback(self.accel_callback)


    def wait_for_multiple_tap(self):
        """
        Store the tap sequence over a 10 second interval. Pass that sequence to\
        the callback function and call the callback function
        """


        # Wait for first touch
        while True:
            if self.accelerometer.tapped:
                logging.info("Single Tap detected")
                break
        # Record touch time
        time_intervals = [time.time()]
        # Record Overall_time
        overall_time = 0
        # Go through the loop until 10 seconds has passed
        while overall_time <= 10:
            beginning_time = time.time()
            if self.accelerometer.tapped:
                logging.info("Single Tap detected")
                # Get current time stamp of when the accelerometer was pressed
                time_intervals.append(time.time())
                # Hope and pray that .1 s is fast enough to capture all the taps
                # Without getting in the users way
                time.sleep(0.1)
            # Record the different between the current time and the strating time
            # of the current loop
            overall_time = time.time() - beginning_time

        self.run_callback(self.accel_callback, value=time_intervals)


    def motion_event(self, data_pin, callback):
        """
        Once motion is detected call the callback function

        :param data_pin : Input pin for the motion sensor
        :param callback : Callable function
        """


        self.data_pin = data_pin
        self.motion_callback = callback
        self.wait_for_motion()


    def wait_for_motion(self):
        """
        Wait for motion to be detected then call callback function
        """


        flag = self.pin_equals_zero()
        while flag:
            flag = self.pin_equal_zero()
        logging.info("Motion Detected")
        self.run_callback(self.motion_callback)


    def pin_equals_zero(self):
        """
        Check if motion sensor detected anything

        :return : boolean representing if the motion sensor detects anything
        """


        # Check if sensor senses something
        if self.data_pin.value == 0:
            return True
        else:
            return False


    def run_callback(self, callback, value=None):
        """
        Call the callback function. If value does not equal None then pass the values\
        to the callback functions

        :param callback : callable function
        :param value : extra parameters needing to be passed to the callback function. Default is None
        """


        logging.info("Callback run for action event")
        # Check is value if callback needs a parameter
        if value == None:
            callback()
        else:
            callback(value)
