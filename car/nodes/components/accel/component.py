# coding=utf-8
"""
Ultrasonic components.
"""
import logging
import os
import time
import math

logger = logging.getLogger()

from helpers import SmBusFactory
from qc import mpu6050
from qc.utils import convert_axes
from ..gpio import GpioComponent


class AccelerometerGyroscopeSensorComponent(GpioComponent):

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
    @todo Provision rpi with arduino-inbox/PyComms
    """

    __CALIBRATION_ITERATIONS = 100

    if os.getenv('CALIBRATION_ITERATIONS'):
        try:
            ci = int(os.getenv('CALIBRATION_ITERATIONS'))
            if ci > __CALIBRATION_ITERATIONS:
                __CALIBRATION_ITERATIONS = ci
        except:
            pass

    def __init__(self):
        GpioComponent.__init__(self)
        self.mpu = mpu6050.MPU6050(
            address=0x68,
            bus=SmBusFactory.build())
        time.sleep(2.0)
        self.mpu.calibrateSensors("./qcoffsets.csv")
        time.sleep(2.0)
        self.mpu.calibrateGyros()
        #-------------------------------------------------------------------------------------------
        # Prime the complementary angle filter with the take-off platform tilt
        #-------------------------------------------------------------------------------------------
        qax_average = 0.0
        qay_average = 0.0
        qaz_average = 0.0
        for loop_count in range(0, 50, 1):
            qax, qay, qaz, qgx, qgy, qgz = self.mpu.readSensors()
            qax_average += qax
            qay_average += qay
            qaz_average += qaz
            time.sleep(0.05)
        qax = qax_average / 50.0
        qay = qay_average / 50.0
        qaz = qaz_average / 50.0

        prev_c_pitch, prev_c_roll, prev_c_tilt  = self.mpu.getEulerAngles(qax, qay, qaz)
        logger.critical("Platform tilt: pitch %f, roll %f", prev_c_pitch * 180 / math.pi, prev_c_roll * 180 / math.pi)

        #-------------------------------------------------------------------------------------------
        # Prime the earth axis accelerometer values for accurate earth axis speed integration
        #-------------------------------------------------------------------------------------------
        eax, eay, eaz = convert_axes(qax, qay, qaz, prev_c_pitch, prev_c_roll)
        eax_offset = eax
        eay_offset = eay
        eaz_offset = eaz

        logger.critical("Platform motion: qax %f, qay %f, qaz %f, g %f", qax, qay, qaz, math.pow(math.pow(qax, 2) + math.pow(qay, 2) + math.pow(qaz, 2), 0.5))
        logger.critical("Platform motion: eax %f, eay %f, eaz %f, g %f", eax, eay, eaz, math.pow(math.pow(eax, 2) + math.pow(eay, 2) + math.pow(1.0 + eaz, 2), 0.5))

        #-------------------------------------------------------------------------------------------
        # Preset the integrated gyro to match the take-off angle
        #-------------------------------------------------------------------------------------------
        i_pitch = prev_c_pitch
        i_roll = prev_c_roll
        i_yaw = 0.0
        # ... tbc





    def reading(self):
        return None, None, None, None
