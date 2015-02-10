#!/usr/bin/env python
# coding=utf-8

import time
import RPIO

TRIG = 24
ECHO = 22
LOOP_DELAY = .2
START_DELAY = .3
PING_DELAY = 0.00001
SOUND_SPEED_Q = 17000

# point the software to the GPIO pins the sensor is using
# change these values to the pins you are using
# GPIO output = the pin that's connected to "Trig" on the sensor
# GPIO input = the pin that's connected to "Echo" on the sensor
RPIO.setup(TRIG, RPIO.OUT)
RPIO.setup(ECHO, RPIO.IN)
RPIO.output(TRIG, False)


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

    if not before_signal and not after_signal:
        return None

    time_passed = after_signal - before_signal
    distance = time_passed * SOUND_SPEED_Q

    return distance


try:
    print "SysInfo: ", RPIO.sysinfo()
    print "Version: ", RPIO.version()
    while True:
        print reading()
        time.sleep(LOOP_DELAY)
except KeyboardInterrupt:
    RPIO.cleanup()
