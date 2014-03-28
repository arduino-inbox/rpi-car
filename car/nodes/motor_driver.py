# coding=utf-8
"""
Motor driver node.
"""

from common import MotorNode
from components import MotorDriverComponent


class MotorDriverNode(MotorNode):
    name = 'Motor Driver Controller'

    def __init__(self, direction, speed):
        MotorNode.__init__(self, direction, speed)
        self.motor_driver_component = MotorDriverComponent()

    def do(self):
        if self.value_proxy.value == MotorNode.FORWARD:
            self.motor_driver_component.forward()
        elif self.value_proxy.value == MotorNode.BACKWARD:
            self.motor_driver_component.backward()
        else:
            self.motor_driver_component.stop()
