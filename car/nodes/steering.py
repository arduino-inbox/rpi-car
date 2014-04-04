# coding=utf-8
"""
Steering servo node.
"""

from common import ServoNode


class SteeringServoNode(ServoNode):
    """
    Steering servo motor node.
    """
    name = 'Steering Servo'

    def __init__(self):
        ServoNode.__init__(self)
