# coding=utf-8
"""
GPIO-related classes
"""
import inspect
import time

class Settings:
    DEBUG = True
    DEBUG_SLEEP = .2


def debug(message):
    if Settings.DEBUG:
        frm = inspect.stack()[2]
        mod = inspect.getmodule(frm[0])
        print mod.__name__, "-", message
        time.sleep(Settings.DEBUG_SLEEP)


class ServoProxy:
    def set_servo(self, pin, value):
        debug("ServoProxy.set_servo - pin: "+str(pin)+", mode: "+str(value))


class PwmProxy:
    def __init__(self):
        self.LOG_LEVEL_ERRORS = 'LOG_LEVEL_ERRORS'
        self.Servo = ServoProxy

    def set_loglevel(self, level):
        debug("PwmProxy.set_loglevel - level: "+str(level))


class GpioProxy:
    def __init__(self):
        self.IN = "Input"
        self.OUT = "Output"
        self.pwm = PwmProxy()
        self._lastInput = False

    def setup(self, pin, mode):
        debug("setup - pin: "+str(pin)+", mode: "+str(mode))

    def input(self, pin):
        debug("input - pin: "+str(pin))
        self._lastInput = not self._lastInput
        return self._lastInput

    def output(self, pin, value):
        debug("output - pin: "+str(pin)+", value: "+str(value))

    def cleanup(self):
        debug("cleanup")


def gpio_factory():
    gpio = GpioProxy()

    try:
        import RPIO
        from RPIO import PWM

        Settings.DEBUG = False
        gpio.setup = RPIO.setup
        gpio.input = RPIO.input
        gpio.output = RPIO.output
        gpio.cleanup = RPIO.cleanup
        gpio.IN = RPIO.IN
        gpio.OUT = RPIO.OUT
        gpio.pwm = PWM
    except Exception, e:
        print e.message
    return gpio


class GpioComponent:
    gpio = None

    def __init__(self):
        self.gpio = gpio_factory()
