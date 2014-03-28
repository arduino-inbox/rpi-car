# coding=utf-8
"""
GPIO-related classes
"""


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

    return gpio


class GpioProxy():
    IN = None
    OUT = None
    pwm = None

    def setup(*args, **kwargs):
        pass

    def input(*args, **kwargs):
        pass

    def output(*args, **kwargs):
        pass

    def cleanup(*args, **kwargs):
        pass


class GpioComponent:
    gpio = None

    def __init__(self):
        self.gpio = gpio_factory()
