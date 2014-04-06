# coding=utf-8
"""
Ultrasonic nodes.
"""

from common import ServoNode, DistanceSensorNode
from components import UltrasonicSensorComponent


class UltrasonicServoNode(ServoNode):
    """
    Ultrasonic sensor rotation servo motor node.
    """
    name = 'Ultrasonic Servo'

    def __init__(self):
        ServoNode.__init__(self)
        # todo Implement
        raise NotImplementedError


class UltrasonicSensorNode(DistanceSensorNode):
    """
    Ultrasonic sensor node.
    """
    name = 'Ultrasonic Sensor'

    def __init__(self):
        DistanceSensorNode.__init__(self)
        self.ultrasonic_sensor_component = UltrasonicSensorComponent()

    def do(self):
        """
        Read ultrasonic component value and update the property.
        """
        self.set_distance(self.ultrasonic_sensor_component.reading())
