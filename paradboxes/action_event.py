"""
Provide an event listener for connect devices

Classes:

ActionEvent()
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
    Allow callback functions to be executed after a sensor is activated.
    Supported sensors include:
    - Accelerometer
    - Motion Sensor

    Functions:

    accelerometer_event(self, accelerometer, callback, sensitivity=60, tap=True, double_tap=False,
    multiple_tap=False, timeout=600)
    motion_event(self, data_pin, callback)
    """

    def __init__(self):
        logging.basicConfig(format="%(message)s %(asctime)s", datefmt=" ---[%m/%d/%y %I:%M:%S %p]", filename="log.log",
                            level=logging.INFO)
        logging.info("ActionEvent Object created")

    def accelerometer_event(self, accelerometer, callback, sensitivity=60, tap=True, double_tap=False, tap_amount=None,
                            multiple_tap=False, timeout=60, multiple_tap_interval=10):
        """
        Call back a given function when the specified action event happens on the accelerometer.\
        You can set multiple action events to be true, but not all the action events \
        will be executed. The order of importance is (Most to Least important):
        Tap, Double Tap, Multiple Tap

        :param accelerometer : A adafruit circuit-python accelerometer object
        :param callback : callable function
        :param sensitivity : sensitivity of the accelerometer. Default is 60, can range from 0 - 100
        :param tap : a single tap of the accelerometer. Action event
        :param double_tap : a double tap of the accelerometer. Action event
        :param tap_amount : amount of times the accelerometer can be tapped until it times out
        :param multiple_tap : records the sequence of taps in a 10 second time period. Action event
        :param timeout : the amount of time that it takes for the wait to timeout. Defaults to 600 seconds
        :param multiple_tap_interval : amount of time that the multitap function will go for. Defaults to 10 seconds
        """

        logging.info("Accelerometer Event created")
        self.accelerometer = accelerometer
        self.accel_callback = callback
        self.timeout = timeout
        self.multiple_tap_interval = multiple_tap_interval
        self.tap_amount = tap_amount

        # Get the type of action that you want to wait for
        if tap:
            self.accelerometer.set_tap(1, sensitivity)
            self.__wait_for_tap()
        elif double_tap:
            self.accelerometer.set_tap(2, sensitivity)
            self.__wait_for_tap()
        elif multiple_tap:
            self.accelerometer.set_tap(1, sensitivity)
            self.__wait_for_multiple_tap()
        elif tap_amount is not None:
            self.accelerometer.set_tap(1, sensitivity)
            self.__wait_for_tap_amount()
        else:
            raise SyntaxError("No action event was set.")

    def __wait_for_tap(self):

        tracker = 0
        called = False
        while tracker < self.timeout:
            time_mark = time.time()

            # If the accelerometer is tapped then call the callback and break from the loop
            if self.accelerometer.tapped:
                logging.info("Tap Detected")
                self.__run_callback(self.accel_callback)
                called = True
                break

            time.sleep(0.1)
            tracker += time.time() - time_mark

        logging.info("Tap timed out.")

        # Make sure that the callback is not called twice
        if not called:
            self.__run_callback(self.accel_callback)

    def __wait_for_multiple_tap(self):

        # Record touch time
        time_intervals = []
        # Record Overall_time
        overall_time = 0
        # Go through the loop until 10 seconds has passed
        while overall_time < self.timeout:
            beginning_time = time.time()
            if self.accelerometer.tapped:
                logging.info("Single Tap detected")
                # Get current time stamp of when the accelerometer was pressed
                time_intervals.append(time.time())
                # Hope and pray that .2 s is fast enough to capture all the taps
                # Without getting in the users way
                time.sleep(0.2)
            # Record the different between the current time and the starting time
            # of the current loop
            overall_time += time.time() - beginning_time

        # Run the callback function after it's recorded all the taps within the time amount
        self.__run_callback(self.accel_callback, value=time_intervals)

    def __wait_for_tap_amount(self):

        # Record Overall_time
        overall_time = 0
        this_tap_count = 0
        # Go through the loop until 10 seconds has passed
        while overall_time <= self.timeout:
            beginning_time = time.time()
            if self.accelerometer.tapped:
                logging.info("Single Tap detected")
                # Hope and pray that .1 s is fast enough to capture all the taps
                # Without getting in the users way
                time.sleep(0.1)
                this_tap_count += 1
            # Record the different between the current time and the starting time
            # of the current loop
            overall_time += time.time() - beginning_time
            if this_tap_count >= self.tap_amount:
                break

        self.run_callback(self.accel_callback, value=this_tap_count)

    def motion_event(self, data_pin, callback):
        """
        Once motion is detected call the callback function

        :param data_pin : Input pin for the motion sensor
        :param callback : Callable function
        """

        self.data_pin = data_pin
        self.motion_callback = callback
        self.__wait_for_motion()

    def __wait_for_motion(self):

        flag = self.__pin_equals_zero()
        while flag:
            flag = self.__pin_equals_zero()
            time.sleep(0.01)
        logging.info("Motion Detected")
        self.__run_callback(self.motion_callback)

    def __pin_equals_zero(self):

        # Check if sensor senses something
        # I have found that some motion sensors output different values. 0 may need to be changed to 1 depending on
        # the motion sensor you are using.
        if self.data_pin.value == 0:
            return True
        else:
            return False

    def __run_callback(self, callback, value=None):
        """
        Call the callback function. If value does not equal None then pass the values\
        to the callback functions

        :param callback : callable function
        :param value : extra parameters needing to be passed to the callback function. Default is None
        """

        logging.info("Callback, {}, run for action event".format(callback))

        # Check if value was passed
        if value is None:
            callback()
        else:
            callback(value)
