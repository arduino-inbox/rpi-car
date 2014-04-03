# coding=utf-8
"""
Main executable of python robot car.
"""
from nodes import MotorDriver, UltrasonicSensorNode, BrainNode, Car


distance_sensor = UltrasonicSensorNode()
motor = MotorDriver()
brain = BrainNode()

nodes = [
    motor,
    distance_sensor,
    brain,
]


Car.run(nodes)