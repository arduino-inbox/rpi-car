# coding=utf-8
"""
GPIO-related classes
"""
import logging

logger = logging.getLogger()


#noinspection PyMethodMayBeStatic,PyClassHasNoInit
class ServoProxy:
    """
    Mock RPIO.PWM.Servo class.
    """
    def set_servo(self, pin, value):
        """
        Mock RPIO.PWM.set_servo.

        @param pin: int
        @param value: int
        """
        logger.debug("ServoProxy.set_servo - pin: "+str(pin)+", value: "+str(
            value))


#noinspection PyMethodMayBeStatic,PyClassHasNoInit
class PwmProxy:
    """
    Mock RPIO.PWM module.
    """

    LOG_LEVEL_ERRORS = 'LOG_LEVEL_ERRORS'
    Servo = ServoProxy

    def set_loglevel(self, level):
        """
        Mock RPIO.PWM.set_loglevel method.

        @param level: object
        """
        logger.debug("PwmProxy.set_loglevel - level: "+str(level))


#noinspection PyMethodMayBeStatic,PyPep8Naming
class GpioProxy:
    """
    GPIO proxy
    """
    def __init__(self):
        self.IN = "Input"
        self.OUT = "Output"
        self.pwm = PwmProxy()
        self._lastInput = False

    def setup(self, pin, mode):
        """
        Mock RPIO.setup method.

        @param pin: int
        @param mode: int
        """
        logger.debug("GpioProxy.setup - pin: "+str(pin)+", mode: "+str(mode))

    def input(self, pin):
        """
        Mock RPIO.input method.

        @param pin: int
        """
        logger.debug("GpioProxy.input - pin: "+str(pin))
        self._lastInput = not self._lastInput
        return self._lastInput

    def output(self, pin, value):
        """
        Mock RPIO.output method.

        @param pin: int
        @param value: int
        """
        logger.debug("GpioProxy.output - pin: "+str(pin)+", value: "+str(value))

    def cleanup(self):
        """
        Mock RPIO.cleanup method.
        """
        logger.debug("GpioProxy.cleanup")


#noinspection PyPep8Naming,PyClassHasNoInit
class GpioFactory:
    """
    GPIO factory.
    """
    @staticmethod
    def build():
        """
        Get GPIO module or its mock.
        @return: GpioProxy
        """
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
            logger.error(e.message)
        return gpio


class GpioComponent:
    """
    Generic GPIO component
    """
    gpio = None

    def __init__(self):
        self.gpio = GpioFactory.build()
