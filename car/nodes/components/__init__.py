# coding=utf-8
"""
Hardware component interface implementations
"""

from ultrasonic import UltrasonicSensorComponent
from motor_driver import MotorDriverComponent
from accel import AccelGyroSensorComponent


if __name__ == "__main__":
    # Testing components
    ultrasonic_sensor_component = UltrasonicSensorComponent()
    while True:
        print "ultrasonic_sensor_component.reading"
        print ultrasonic_sensor_component.reading()
