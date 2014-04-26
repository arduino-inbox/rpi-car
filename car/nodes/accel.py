# coding=utf-8
"""
Accelerometer/Gyro sensor node.
"""
from cmath import sqrt
from components.constants import CHANNEL_TRAVEL_DISTANCE
from components import AccelerometerGyroscopeSensorComponent
from common import PublisherNode, timestamp


class AccelerometerGyroscopeSensorNode(PublisherNode):
    """
    Accelerometer/Gyroscope node.
    """
    name = 'Accelerometer/Gyroscope Sensor'

    def __init__(self):
        PublisherNode.__init__(self)
        self.sensor_component = AccelerometerGyroscopeSensorComponent()
        self.t0 = timestamp(precision=9)
        self.xTravel = 0
        self.yTravel = 0
        self.zTravel = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.zVelocity = 0

    def do(self):
        """
        Read component value and update the property.
        """
        fax, fay, faz, fgx, fgy, fgz = self.sensor_component.reading()
        self.t1 = timestamp(precision=9)
        deltaTime = self.t1 - self.t0

        # convert to force [N]
        ax = fax * 9.80665
        ay = fay * 9.80665
        #az *= 9.80665

        # distance moved in deltaTime, s = 1/2 a t^2 + vt
        sx = 0.5 * ax * deltaTime * deltaTime + self.xVelocity * deltaTime
        sy = 0.5 * ay * deltaTime * deltaTime + self.yVelocity * deltaTime
        #sz = 0.5 * az * deltaTime * deltaTime + self.zVelocity * deltaTime
        self.xTravel += sx
        self.yTravel += sy
        #self.zTravel += sz

        # change in velocity, v = v0 + at
        self.xVelocity += ax * deltaTime
        self.yVelocity += ay * deltaTime
        #self.zVelocity += az * deltaTime

        #
        travel = sqrt(self.xTravel ** 2 + self.yTravel ** 2)

        # Update t0
        self.t0 = self.t1

        # set
        self.send(CHANNEL_TRAVEL_DISTANCE, travel)

