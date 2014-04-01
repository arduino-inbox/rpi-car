# coding=utf-8
"""
GPIO-related classes
"""
import inspect
import time


def gpio_factory():
    gpio = GpioProxy()

    try:
        import RPIO
        from RPIO import PWM

        gpio.setup = RPIO.setup
        gpio.input = RPIO.input
        gpio.output = RPIO.output
        gpio.cleanup = RPIO.cleanup
        gpio.IN = RPIO.IN
        gpio.OUT = RPIO.OUT
        gpio.pwm = PWM
    except Exception, e:
        print e.message
        gpio.DEBUG = True
    return gpio


class GpioProxy():
    DEBUG = False
    IN = "Input"
    OUT = "Output"
    pwm = None
    _lastInput = True
    DEBUG_SLEEP = .5

    def setup(self, *args):
        self._debug("setup - pin: "+str(args[0])+", mode: "+str(args[1]))

    def input(self, *args):
        self._debug("input - pin: "+str(args[0]))
        self._lastInput = not self._lastInput
        return self._lastInput

    def output(self, *args):
        self._debug("output - pin: "+str(args[0])+", value: "+str(args[1]))

    def cleanup(self):
        self._debug("cleanup")

    def _debug(self, message):
        if self.DEBUG:
            frm = inspect.stack()[2]
            mod = inspect.getmodule(frm[0])
            print mod.__name__, "-", message
            time.sleep(self.DEBUG_SLEEP)


class GpioComponent:
    gpio = None

    def __init__(self):
        self.gpio = gpio_factory()
