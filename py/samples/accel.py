#!/usr/bin/python
# coding=utf-8

import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68        # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

from redis import StrictRedis
redis_conn = StrictRedis(host='localhost', port=6379, db=0)

while True:
    gyro = (read_word_2c(0x43), read_word_2c(0x45), read_word_2c(0x47),)
    accel = (read_word_2c(0x3b), read_word_2c(0x3d), read_word_2c(0x3f),)
    redis_conn.set('test-gyro-0', gyro[0])
    redis_conn.set('test-gyro-1', gyro[1])
    redis_conn.set('test-gyro-2', gyro[2])
    redis_conn.set('test-accel-0', accel[0])
    redis_conn.set('test-accel-1', accel[1])
    redis_conn.set('test-accel-2', accel[2])

    #accel_xout_scaled = accel_xout / 16384.0

    # print (
    #     "gyro: ", gyro,  # " scaled: ", (gyro_xout / 131)
    #     "accel: ", accel,  # " scaled: ", accel_xout_scaled
    # )

    #print (
    #    "x rotation: ",
    #    get_x_rotation(
    #        accel_xout_scaled, accel_yout_scaled, accel_zout_scaled
    #    ),
    #    "y rotation: ",
    #    get_y_rotation(
    #        accel_xout_scaled, accel_yout_scaled, accel_zout_scaled
    #    )
    #)
