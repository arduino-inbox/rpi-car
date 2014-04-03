# coding=utf-8
"""
Ultrasonic nodes.
"""

from common import ServoNode, DistanceSensor, Subscriber
from components import UltrasonicSensorComponent


class UltrasonicServoNode(ServoNode):
    name = 'Ultrasonic Servo'


class UltrasonicSensorNode(DistanceSensor, Subscriber):
    name = 'Ultrasonic Sensor'

    def __init__(self):
        DistanceSensor.__init__(self)
        Subscriber.__init__(self, [])
        self.ultrasonic_sensor_component = UltrasonicSensorComponent()

    def do(self):
        self.set_distance(self.ultrasonic_sensor_component.reading())
