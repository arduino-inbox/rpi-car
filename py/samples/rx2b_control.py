#!/usr/bin/env python
# coding=utf-8
import time

import RPIO
gpio_setup = RPIO.setup
gpio_output = RPIO.output
gpio_cleanup = RPIO.cleanup
OUT = RPIO.OUT

SI_PIN = 25

gpio_setup(SI_PIN, OUT)
gpio_output(SI_PIN, False)

W2_ON = 0.0015
W2_OFF = 0.0005

W1_ON = 0.0005
W1_OFF = 0.0005

CMD_START = 4
CMD_FORWARD = 10
CMD_BACKWARD = 40


def command(cmd, on, off):
    for w in xrange(cmd):
        gpio_output(SI_PIN, True)
        time.sleep(on)
        gpio_output(SI_PIN, False)
        time.sleep(off)

def mark():
    command(CMD_START, W2_ON, W2_OFF)

def move(cmd):
    mark()
    command(cmd, W1_ON, W1_OFF)

def forward():
    move(CMD_FORWARD)

def backward():
    move(CMD_BACKWARD)


try:
    while True:
        forward()

except KeyboardInterrupt:
    gpio_cleanup()
