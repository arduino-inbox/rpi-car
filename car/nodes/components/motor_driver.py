# coding=utf-8
"""
Motor driver component
"""

from gpio import GpioComponent

SPEED_PWM_PIN = 25
IN1_PIN = 17
IN2_PIN = 27

SPEED_STEP = 100
MIN_SPEED = 4000
MAX_SPEED = 6000


class MotorDriverComponent(GpioComponent):

    def __init__(self, speed_pin=SPEED_PWM_PIN, in1_pin=IN1_PIN,
                 in2_pin=IN2_PIN):
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
