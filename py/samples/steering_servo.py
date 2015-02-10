#!/usr/bin/env python
# coding=utf-8

from RPIO import PWM
import time

SERVO_WAIT = .3
PW_NEUTRAL = 1850
PW_LIMIT = 260
PW_MIN_LIMIT = PW_NEUTRAL - PW_LIMIT
PW_MAX_LIMIT = PW_NEUTRAL + PW_LIMIT

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
