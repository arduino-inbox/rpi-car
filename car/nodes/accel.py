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
        for result in self.sensor_component.reading():
            (self.dt, self.yaw, self.ax, self.ay) = result
            if self.dt and self.yaw and self.ax and self.ay:
                logger.debug(
                    "∂t={dt}s, Yaw={yaw}, aX={ax}, aY={ay}"
                    .format(
                        dt=self.dt, yaw=self.yaw,
                        ax=self.ax, ay=self.ay))

            #    self.axy = float(math.sqrt(self.ax**2 + self.ay**2).real)
            #
            #    # change in velocity, v = v0 + at
            #    self.vx += self.ax * self.dt
            #    self.vy += self.ay * self.dt
            #    self.vxy = float(math.sqrt(self.vx**2 + self.vy**2).real)
            #
            #    # distance moved in deltaTime, s = 1/2 a t^2 + vt
            #    self.sx = 0.5 * self.ax * self.dt * self.dt + self.vx * self.dt
            #    self.sy = 0.5 * self.ay * self.dt * self.dt + self.vy * self.dt
            #    self.tx += self.sx
            #    self.ty += self.sy
            #    self.txy = float(math.sqrt(self.tx ** 2 + self.tx ** 2).real)
            #
            #self.send(CHANNEL_ACCELERATION, self.axy)
            #self.send(CHANNEL_TRAVEL_VELOCITY, self.vxy)
            #self.send(CHANNEL_TRAVEL_DISTANCE, self.txy)
