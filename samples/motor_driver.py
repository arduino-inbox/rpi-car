#!/usr/bin/env python
# coding=utf-8
import time

import RPIO
from RPIO import PWM
gpio_setup = RPIO.setup
gpio_output = RPIO.output
gpio_cleanup = RPIO.cleanup
OUT = RPIO.OUT

SPEED_PWM_PIN = 25
IN1_PIN = 17
IN2_PIN = 27

try:
    # gpio_output(SPEED_PWM_PIN, True)
    while True:
        gpio_output(IN2_PIN, False)
        gpio_output(IN1_PIN, True)
        # time.sleep(3)
        gpio_output(IN1_PIN, False)
        gpio_output(IN2_PIN, True)
        time.sleep(1)
        speed += SPEED_STEP
        if speed > MAX_SPEED:
            speed = MIN_SPEED
        print "Speed: ", speed
        servo.set_servo(SPEED_PWM_PIN, speed)
        # time.sleep(5)
        # gpio_output(IN1_PIN, False)
        # gpio_output(IN2_PIN, False)
        # time.sleep(5)


except KeyboardInterrupt:
    gpio_cleanup()
