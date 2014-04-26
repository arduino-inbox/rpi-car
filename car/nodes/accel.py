# coding=utf-8
"""
Accelerometer/Gyro sensor node.
"""
import cmath
# import time
from components.constants import *
from components import AccelerometerGyroscopeSensorComponent
from common import PublisherNode


class AccelerometerGyroscopeSensorNode(PublisherNode):
    """
    Accelerometer/Gyroscope node.
    """
    name = 'Accelerometer/Gyroscope Sensor'

    def __init__(self):
        PublisherNode.__init__(self)
        self.sensor_component = AccelerometerGyroscopeSensorComponent()
        # self.t0 = None
        # self.xTravel = 0
        # self.yTravel = 0
        # self.zTravel = 0
        # self.xVelocity = 0
        # self.yVelocity = 0
        # self.zVelocity = 0

    def do(self):
        """
        Read component value and update the property.
        """
        # if self.t0 is None:
        #     self.t0 = time.time()

        fax, fay, faz, fgx, fgy, fgz = self.sensor_component.reading()
        # self.t1 = time.time()
        # deltaTime = self.t1 - self.t0

        # convert to force [N]
        ax = fax * 9.80665
        ay = fay * 9.80665

        self.send(CHANNEL_ACCELERATION, float(cmath.sqrt(ax**2 + ay**2).real))

        #az *= 9.80665

        # # distance moved in deltaTime, s = 1/2 a t^2 + vt
        # sx = 0.5 * ax * deltaTime * deltaTime + self.xVelocity * deltaTime
        # sy = 0.5 * ay * deltaTime * deltaTime + self.yVelocity * deltaTime
        # #sz = 0.5 * az * deltaTime * deltaTime + self.zVelocity * deltaTime
        # self.xTravel += sx
        # self.yTravel += sy
        # #self.zTravel += sz
        #
        # # change in velocity, v = v0 + at
        # self.xVelocity += ax * deltaTime
        # self.yVelocity += ay * deltaTime
        # #self.zVelocity += az * deltaTime
        #
        # #
        # travel = cmath.sqrt(self.xTravel ** 2 + self.yTravel ** 2).real
        #
        # # Update t0
        # self.t0 = self.t1
        #
        # # set
        # self.send(CHANNEL_TRAVEL_DISTANCE, float(travel))

