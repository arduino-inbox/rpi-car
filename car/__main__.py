# coding=utf-8
"""
Main executable of python robot car.
"""
from nodes.components.gpio import GpioFactory
from nodes import (MotorDriverNode, UltrasonicSensorNode, BrainNode, Car, AccelerometerGyroscopeSensorNode,
                   BluetoothNode)

# Logging setup
import logging
import os

logger = logging.getLogger()
if os.environ.get('DEBUG'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.CRITICAL)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(process)d/%(processName)s: %(asctime)-15s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Cleanup previously defined GPIO settings
GpioFactory.build().cleanup()

# distance_sensor = UltrasonicSensorNode()
# motor = MotorDriverNode()
# brain = BrainNode()
# bt = BluetoothNode()
accel_gyro = AccelerometerGyroscopeSensorNode()

nodes = [
    # motor,
    # distance_sensor,
    # brain,
    accel_gyro,
    # bt,
]

Car.run(nodes)