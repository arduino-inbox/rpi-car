# coding=utf-8
"""
Accelerometer/Gyro sensor node.
"""
from components import AccelerometerGyroscopeSensorComponent
from common import PublisherNode


class AccelerometerGyroscopeSensorNode(PublisherNode):
    """
    Accelerometer/Gyroscope node.
    """
    name = 'Accelerometer/Gyroscope Sensor'

    def __init__(self):
        PublisherNode.__init__(self)
        self.sensor_component = AccelerometerGyroscopeSensorComponent()

    def do(self):
        """
        Read ultrasonic component value and update the property.
        """
        self.set_distance(self.ultrasonic_sensor_component.reading())
