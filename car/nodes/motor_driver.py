# coding=utf-8
"""
Motor driver node.
"""
from components.constants import *
from . import SubscriberNode
from components import MotorDriverComponent


class MotorDriverNode(SubscriberNode):
    """
    Motor driver node.
    """

    name = 'Motor Driver Controller'
    channels = [
        'speed',
        'direction',
    ]

    def __init__(self):
        SubscriberNode.__init__(self, self.channels)
        self.motor_driver_component = MotorDriverComponent()
        self.speed = 0
        self.direction = MOTOR_DIRECTION_STOP
        self.data[CHANNEL_SPEED] = self.speed
        self.data[CHANNEL_DIRECTION] = self.direction

    def do(self):
        """
        Read the data and update the motor driver component.
        """

        # Update data.
        SubscriberNode.do(self)

        self.speed = int(self.data[CHANNEL_SPEED])
        self.direction = int(self.data[CHANNEL_DIRECTION])

        if self.direction == MOTOR_DIRECTION_FORWARD:
            self.motor_driver_component.forward(self.speed)
        elif self.direction == MOTOR_DIRECTION_BACKWARD:
            self.motor_driver_component.backward(self.speed)
        else:
            self.motor_driver_component.stop()
