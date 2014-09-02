# coding=utf-8
"""
Accelerometer/Gyro sensor node.
"""
from components.constants import *
from components import AccelerometerGyroscopeSensorComponent
from common import PublisherNode

import logging
logger = logging.getLogger()


class AccelerometerGyroscopeSensorNode(PublisherNode):
    """
    Accelerometer/Gyroscope node.
    """
    name = 'Accelerometer/Gyroscope Sensor'

    def __init__(self):
        PublisherNode.__init__(self)
        self.sensor_component = AccelerometerGyroscopeSensorComponent()

        self.dt = None
        self.yaw = None
        self.a = None
        self.v = None
        self.d = None

    def do(self):
        """
        Read component value and update the property.
        """
        (self.dt, self.yaw, self.a, self.v, self.d) = self.sensor_component.reading()

        self.send(CHANNEL_ROTATION, self.yaw)
        self.send(CHANNEL_ACCELERATION, self.a)
        self.send(CHANNEL_TRAVEL_VELOCITY, self.v)
        self.send(CHANNEL_TRAVEL_DISTANCE, self.d)
