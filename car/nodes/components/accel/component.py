# coding=utf-8
"""
Ultrasonic components.
"""
from helpers import MPU6050
from ..gpio import GpioComponent


class AccelerometerGyroSensorComponent(GpioComponent):

    """
    @todo Read these:
     - http://www.botched.co.uk/pic-tutorials/mpu6050-setup-data-aquisition/
     - http://marks-space.com/2013/04/29/guide-to-interfacing-a-gyro-and-accelerometer-with-a-raspberry-pi/
     - https://github.com/mwilliams03/Raspberry-Gyro-Acc
     - http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html
     - Connecting MPU-6050 to RPI: http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
     - http://www.raspberrypi.org/forums/viewtopic.php?t=22266
     - http://randomsenseless.blogspot.com/2013/06/arduino-based-inertial-navigation.html
     - http://www.i2cdevlib.com/forums/topic/91-how-to-decide-gyro-and-accelerometer-offsett/
     - http://www.i2cdevlib.com/forums/topic/4-understanding-raw-values-of-accelerometer-and-gyrometer/
     - http://mpuprojectblog.wordpress.com/2013/01/31/distance-measurement/

    @todo Provision rpi for i2c use.
    """

    def __init__(self):
        GpioComponent.__init__(self)
        self.mpu = MPU6050()

    def reading(self):
        """
        Read accelerometer/gyroscope values.
        @return:
        """
        return self.mpu.read_sensors()
