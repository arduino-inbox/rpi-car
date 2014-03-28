# coding=utf-8
"""
Ultrasonic nodes.
"""

from common import ServoNode, DistanceSensorNode
from components import UltrasonicSensorComponent


class UltrasonicServoNode(ServoNode):
    name = 'Ultrasonic Servo'


class UltrasonicSensorNode(DistanceSensorNode):
    name = 'Ultrasonic Sensor'

    def __init__(self, value_proxy):
        DistanceSensorNode.__init__(self, value_proxy)
        self.ultrasonic_sensor_component = UltrasonicSensorComponent()

    def do(self):
        self.value_proxy.value = self.ultrasonic_sensor_component.reading()
        print self.value_proxy.value
