# coding=utf-8
"""
GPIO-related classes
"""
import logging

logger = logging.getLogger()


class ServoProxy:
    def set_servo(self, pin, value):
        logger.debug("ServoProxy.set_servo - pin: "+str(pin)+", mode: "+str(value))



class PwmProxy:
    def __init__(self):
        self.LOG_LEVEL_ERRORS = 'LOG_LEVEL_ERRORS'
        self.Servo = ServoProxy

    def set_loglevel(self, level):
        logger.debug("PwmProxy.set_loglevel - level: "+str(level))


class GpioProxy:
    def __init__(self):
        self.IN = "Input"
        self.OUT = "Output"
        self.pwm = PwmProxy()
        self._lastInput = False

    def setup(self, pin, mode):
        logger.debug("GpioProxy.setup - pin: "+str(pin)+", mode: "+str(mode))

    def input(self, pin):
        logger.debug("GpioProxy.input - pin: "+str(pin))
        self._lastInput = not self._lastInput
        return self._lastInput

    def output(self, pin, value):
        logger.debug("GpioProxy.output - pin: "+str(pin)+", value: "+str(value))

    def cleanup(self):
        logger.debug("GpioProxy.cleanup")


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
        logger.setLevel(logging.DEBUG)
        logger.error(e.message)
    return gpio


class GpioComponent:
    gpio = None

    def __init__(self):
        self.gpio = gpio_factory()
