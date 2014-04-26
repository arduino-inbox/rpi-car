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
        Read component value and update the property.
        """
        fax, fay, faz, fgx, fgy, fgz = self.sensor_component.reading()
