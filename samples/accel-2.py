#!/usr/bin/python
# coding=utf-8

import smbus
import math


import time
import math
import mpu6050

# Sensor initialization
mpu = mpu6050.MPU6050()
mpu.dmpInitialize()
mpu.setDMPEnabled(True)

# get expected DMP packet size for later comparison
packetSize = mpu.dmpGetFIFOPacketSize()

from redis import StrictRedis
redis_conn = StrictRedis(host='localhost', port=6379, db=0)


while True:
    # Get INT_STATUS byte
    mpuIntStatus = mpu.getIntStatus()

    if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently)
        # get current FIFO count
        fifoCount = mpu.getFIFOCount()

        # check for overflow (this should never happen unless our code is too inefficient)
        if fifoCount == 1024:
            # reset so we can continue cleanly
            mpu.resetFIFO()
            print('FIFO overflow!')


        # wait for correct available data length, should be a VERY short wait
        fifoCount = mpu.getFIFOCount()
        while fifoCount < packetSize:
            fifoCount = mpu.getFIFOCount()

        result = mpu.getFIFOBytes(packetSize)
        q = mpu.dmpGetQuaternion(result)
        g = mpu.dmpGetGravity(q)
        ypr = mpu.dmpGetYawPitchRoll(q, g)
        a = mpu.dmpGetAccel(result)
        accel = mpu.dmpGetLinearAccel(a, g)

        y = ypr['yaw'] * 180 / math.pi
        p = ypr['pitch'] * 180 / math.pi
        r = ypr['roll'] * 180 / math.pi

        redis_conn.set('yaw', y)
        redis_conn.set('pitch', p)
        redis_conn.set('roll', r)
        redis_conn.set('accel-x', accel['x'])
        redis_conn.set('accel-y', accel['y'])
        #redis_conn.set('accel-z', accel['z'])

        # track FIFO count here in case there is > 1 packet available
        # (this lets us immediately read more without waiting for an interrupt)
        fifoCount -= packetSize
