# coding=utf-8
"""
Motor driver component
"""

from constants import *
from gpio import GpioComponent


class MotorDriverComponent(GpioComponent):
    """
    Motor driver component.
    """

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

    def forward(self, speed):
        """
        Drive forward with a given speed.

        @param speed: int
        """
        self.gpio.output(self.in2_pin, False)
        self.gpio.output(self.in1_pin, True)
        self.set_speed(speed)

    def backward(self, speed):
        """
        Drive backward with a given speed.

        @param speed: int
        """
        self.gpio.output(self.in1_pin, False)
        self.gpio.output(self.in2_pin, True)
        self.set_speed(speed)

    def stop(self):
        """
        Stop the motor.
        """
        self.gpio.output(self.in1_pin, False)
        self.gpio.output(self.in2_pin, False)
        self.set_speed(0)

    def set_speed(self, value):
        """
        Set PWM value for speed change.
        @param value: int
        """

        # some hack
        if value > 99999:
            value = 99999
        self.speed_servo.set_servo(self.speed_pin, value)
