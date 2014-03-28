# coding=utf-8
"""
Ultrasonic components.
"""

import time
from gpio import GpioComponent

# Some module "constants"
SOUND_SPEED_Q = 17000
MAX_DISTANCE = 2000


class UltrasonicSensorComponent(GpioComponent):
    TRIG = 24
    ECHO = 22
    LOOP_DELAY = 1
    START_DELAY = .3
    PING_DELAY = 0.00001

    trigger_pin = None
    echo_pin = None

    def __init__(self, trigger_pin=TRIG, echo_pin=ECHO):
        GpioComponent.__init__(self)

        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        self.gpio.setup(self.trigger_pin, self.gpio.OUT)
        self.gpio.setup(self.echo_pin, self.gpio.IN)
        self.gpio.output(self.trigger_pin, False)

    def reading(self):
        # found that the sensor can crash if there isn't a delay here
        # no idea why. If you have odd crashing issues, increase delay
        time.sleep(self.START_DELAY)

        self.gpio.output(self.trigger_pin, True)
        time.sleep(self.PING_DELAY)
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
            return MAX_DISTANCE

        time_passed = after_signal - before_signal
        distance = time_passed * SOUND_SPEED_Q

        return distance
