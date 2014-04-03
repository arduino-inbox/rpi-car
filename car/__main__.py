# coding=utf-8
"""
Main executable of python robot car.
"""
from nodes import MotorDriver, UltrasonicSensorNode, BrainNode, Car

# Logging setup
import logging
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


distance_sensor = UltrasonicSensorNode()
motor = MotorDriver()
brain = BrainNode()

nodes = [
    motor,
    distance_sensor,
    brain,
]


Car.run(nodes)