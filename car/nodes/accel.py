# coding=utf-8
"""
Accelerometer/Gyro sensor node.
"""
import math
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
        self.ax = None
        self.ay = None

        self.sx = 0.0
        self.sy = 0.0
        self.tx = 0.0
        self.ty = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.axy = 0.0
        self.vxy = 0.0
        self.txy = 0.0

    def do(self):
        """
        Read component value and update the property.
        """
        (self.dt, self.yaw, self.ax, self.ay) = self.sensor_component.reading()

        self.send(CHANNEL_ACCELERATION, self.ax)
        self.send(CHANNEL_ROTATION, self.yaw)
        self.send(CHANNEL_TRAVEL_VELOCITY, self.vxy)
        self.send(CHANNEL_TRAVEL_DISTANCE, self.txy)
