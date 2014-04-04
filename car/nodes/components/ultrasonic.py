# coding=utf-8
"""
Ultrasonic components.
"""

import time
from constants import *
from gpio import GpioComponent


class UltrasonicSensorComponent(GpioComponent):
    """
    HC-SR04 ultrasonic sensor component.
    """

    def __init__(self, trigger_pin=PIN_ULTRASONIC_TRIG,
                 echo_pin=PIN_ULTRASONIC_ECHO):
        GpioComponent.__init__(self)

        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        self.gpio.setup(self.trigger_pin, self.gpio.OUT)
        self.gpio.setup(self.echo_pin, self.gpio.IN)
        self.gpio.output(self.trigger_pin, False)

    def reading(self):
        """
        Operate the sensor to calculate the distance value.

        @return: float
        """

        # found that the sensor can crash if there isn't a delay here
        # no idea why. If you have odd crashing issues, increase delay
        time.sleep(ULTRASONIC_START_DELAY)

        self.gpio.output(self.trigger_pin, True)
        time.sleep(ULTRASONIC_PING_DELAY)
        self.gpio.output(self.trigger_pin, False)

        before_signal = None
        after_signal = None
        time_start = time.clock()
        while not self.gpio.input(self.echo_pin):
            before_signal = time.time()

        while self.gpio.input(self.echo_pin):
            after_signal = time.time()
            timeout = time.clock() - time_start
            if timeout > 1.0:
                break

        if not before_signal or not after_signal:
            return DISTANCE_MAXIMUM

        time_passed = after_signal - before_signal
        distance = time_passed * ULTRASONIC_SOUND_SPEED_Q

        return distance
