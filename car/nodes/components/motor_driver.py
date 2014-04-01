# coding=utf-8
"""
Motor driver component
"""

from constants import *
from gpio import GpioComponent


class MotorDriverComponent(GpioComponent):
    def __init__(self, speed_pin=PIN_MOTOR_SPEED_PWM,
                 in1_pin=PIN_MOTOR_IN1,
                 in2_pin=PIN_MOTOR_IN2):
        GpioComponent.__init__(self)

        self.speed_pin = speed_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        self.gpio.setup(self.in1_pin, self.gpio.OUT)
        self.gpio.setup(self.in2_pin, self.gpio.OUT)

        self.gpio.pwm.set_loglevel(self.gpio.pwm.LOG_LEVEL_ERRORS)
        self.speed_servo = self.gpio.pwm.Servo()

        self.stop()

    def forward(self):
        self.gpio.output(self.in2_pin, False)
        self.gpio.output(self.in1_pin, True)

    def backward(self):
        self.gpio.output(self.in1_pin, False)
        self.gpio.output(self.in2_pin, True)

    def stop(self):
        self.gpio.output(self.in1_pin, False)
        self.gpio.output(self.in2_pin, False)
        self.set_speed(0)

    def set_speed(self, value):
        self.speed_servo.set_servo(self.speed_pin, value)
