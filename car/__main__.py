# coding=utf-8
"""
Main executable of python robot car.
"""
from nodes import (MotorDriverNode, UltrasonicSensorNode, BrainNode, Car,
                   AccelerometerGyroscopeSensorNode)

# Logging setup
import logging
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


distance_sensor = UltrasonicSensorNode()
motor = MotorDriverNode()
brain = BrainNode()
accelGyro = AccelerometerGyroscopeSensorNode()

nodes = [
    motor,
    distance_sensor,
    brain,
    accelGyro,
]


Car.run(nodes)