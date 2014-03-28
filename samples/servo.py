#!/usr/bin/env python
# coding=utf-8

from RPIO import PWM
import time

SERVO_WAIT = .3
PW_LIMIT = 700
PW_MIN = 500
PW_MAX = 2400
PW_NEUTRAL = 1450 #(PW_MAX + PW_MIN) / 2
PW_MIN_LIMIT = PW_MIN + PW_LIMIT
PW_MAX_LIMIT = PW_MAX - PW_LIMIT

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
        for pin in servo_pins:
            servos[pin].set_servo(pin, PW_MIN_LIMIT)
        time.sleep(SERVO_WAIT)
        for pin in servo_pins:
            servos[pin].set_servo(pin, PW_NEUTRAL)
        time.sleep(SERVO_WAIT)
        for pin in servo_pins:
            servos[pin].set_servo(pin, PW_MAX_LIMIT)
        time.sleep(SERVO_WAIT)
except KeyboardInterrupt:
    for pin in servo_pins:
        servos[pin].stop_servo(pin)
    exit()
