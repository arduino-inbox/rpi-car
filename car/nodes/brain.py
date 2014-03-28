# coding=utf-8
"""
Brain node.
"""
import time
from common import Node, MotorNode


class BrainNode(Node):
    name = 'Brain'
    distance = None
    direction = None
    speed = None
    turn = None

    def __init__(self, distance, direction, speed, turn):
        """
        @type distance: Value
        @type direction: Value
        @type speed: Value
        @type turn: Value
        """
        self.distance = distance
        self.direction = direction
        self.speed = speed

        # @todo Use for servo
        self.turn = turn

        Node.__init__(self)

    def do(self):
        if self.distance.value < 50:
            self.speed.value = 0
            self.direction.value = MotorNode.STOP
        else:
            self.speed.value += 500
            self.direction.value = MotorNode.FORWARD
