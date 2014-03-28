# coding=utf-8
"""
Ultrasonic components.
"""

from gpio import GpioComponent


class AccelGyroSensorComponent(GpioComponent):

    def __init__(self):
        GpioComponent.__init__(self)
        raise NotImplementedError()

    def reading(self):
        raise NotImplementedError()
