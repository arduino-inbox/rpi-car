#!/usr/bin/env python
# coding=utf-8
import time

import RPIO
from RPIO import PWM

TRIG = 24
ECHO = 22
LOOP_DELAY = 1
START_DELAY = .3
PING_DELAY = 0.00001
SOUND_SPEED_Q = 17000

SERVO_WAIT = .2
PW_NEUTRAL = 1500
PW_LIMIT = 460
PW_MIN_LIMIT = PW_NEUTRAL - PW_LIMIT
PW_MAX_LIMIT = PW_NEUTRAL + PW_LIMIT
SERVO_PIN = 18

RPIO.setup(TRIG, RPIO.OUT)
RPIO.setup(ECHO, RPIO.IN)
RPIO.output(TRIG, False)
# SERVO = PWM.Servo()
# SERVO.set_servo(SERVO_PIN, PW_NEUTRAL)

# Turn off debug output
# PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

def reading():
    # found that the sensor can crash if there isn't a delay here
    # no idea why. If you have odd crashing issues, increase delay
    time.sleep(START_DELAY)

    RPIO.output(TRIG, True)
    time.sleep(PING_DELAY)
    RPIO.output(TRIG, False)

    before_signal = None
    after_signal = None

    while not RPIO.input(ECHO):
        before_signal = time.time()

    while RPIO.input(ECHO):
        after_signal = time.time()

    if not before_signal or not after_signal:
        return None

    time_passed = after_signal - before_signal
    distance = time_passed * SOUND_SPEED_Q

    return distance


print "SysInfo: ", RPIO.sysinfo()
print "Version: ", RPIO.version()
while True:
    # SERVO.set_servo(SERVO_PIN, PW_NEUTRAL)
    print "Neutral:", reading()
    # time.sleep(SERVO_WAIT)

    # SERVO.set_servo(SERVO_PIN, PW_MIN_LIMIT)
    # print "Min:", reading()
    # time.sleep(SERVO_WAIT)
    #
    # SERVO.set_servo(SERVO_PIN, PW_NEUTRAL)
    # print "Neutral:", reading()
    # time.sleep(SERVO_WAIT)
    #
    # SERVO.set_servo(SERVO_PIN, PW_MAX_LIMIT)
    # print "Max:", reading()
    # time.sleep(SERVO_WAIT)

    time.sleep(LOOP_DELAY)

