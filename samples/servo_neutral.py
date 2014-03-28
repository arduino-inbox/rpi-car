#!/usr/bin/env python
# coding=utf-8

from RPIO import PWM
import time

SERVO_WAIT = .3
PW_LIMIT = 300
PW_NEUTRAL = 1450

servo_pins = [18] #, 23]
servos = {}
for pin in servo_pins:
    servo = PWM.Servo()
    servo.set_servo(pin, PW_NEUTRAL)
    servos[pin] = servo

try:
    while True:
        for pin in servo_pins:
            servos[pin].set_servo(pin, PW_NEUTRAL)
        time.sleep(SERVO_WAIT)
except KeyboardInterrupt:
    for pin in servo_pins:
        servos[pin].stop_servo(pin)
    exit()
