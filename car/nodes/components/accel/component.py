# coding=utf-8
"""
Ultrasonic components.
"""
import logging
import os
from mpu6050 import MPU6050

logger = logging.getLogger()

from helpers import SmBusFactory
from qc import mpu6050
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


    def reading(self):
        # while True:
        #     # Get INT_STATUS byte
        #     self.mpu_int_status = self.mpu.getIntStatus()
        #
        #     if self.mpu_int_status >= 2:  # check for DMP data ready interrupt
        #         # get current FIFO count
        #         self.fifo_count = self.mpu.getFIFOCount()
        #
        #         # check for overflow
        #         if self.fifo_count == 1024:
        #             # reset so we can continue cleanly
        #             self.mpu.resetFIFO()
        #             logger.warning('FIFO overflow!')
        #
        #         # wait for correct available data length
        #         self.fifo_count = self.mpu.getFIFOCount()
        #         while self.fifo_count < self.packet_size:
        #             self.fifo_count = self.mpu.getFIFOCount()
        #
        #         self.result = self.mpu.getFIFOBytes(self.packet_size)
        #         self.q = self.mpu.dmpGetQuaternion(self.result)
        #         self.g = self.mpu.dmpGetGravity(self.q)
        #         self.ypr = self.mpu.dmpGetYawPitchRoll(self.q, self.g)
        #         self.a = self.mpu.dmpGetAccel(self.result)
        #         self.la = self.mpu.dmpGetLinearAccel(self.a, self.g)
        #         self.laiw = self.mpu.dmpGetLinearAccelInWorld(self.a, self.q)
        #
        #         self.yaw = self.ypr['yaw'] * 180 / math.pi  # rads to degs
        #         self.pitch = self.ypr['pitch'] * 180 / math.pi
        #         self.roll = self.ypr['roll'] * 180 / math.pi
        #         #self.ax = self.la['x'] - self.ax_offset
        #         #self.ay = self.la['y'] - self.ay_offset
        #         #self.az = self.la['z'] - self.az_offset
        #         self.ax = self.laiw['x'] - self.ax_offset
        #         self.ay = self.laiw['y'] - self.ay_offset
        #         self.az = self.laiw['z'] - self.az_offset
        #         # Update timedelta
        #         self.dt = time() - self.t0
        #
        #         # track FIFO count here in case there is > 1 packet available
        #         # (this lets us immediately read more without waiting for an
        #         # interrupt)
        #         self.fifo_count -= self.packet_size
        #
        #         if self.calibrating:
        #             if self._equal(
        #                     [self.yaw, self.pitch, self.roll, self.ax, self.ay,
        #                      self.az, ],
        #                     [self.yaw0, self.pitch0, self.roll0, self.ax0,
        #                      self.ay0, self.az0, ]
        #             ):
        #                 self.calibrating = False
        #                 self.ax_offset = self.ax
        #                 self.ay_offset = self.ay
        #                 self.az_offset = self.az
        #                 self.t0 = time()
        #                 logger.debug("Calibration done in {t}s".format(
        #                     t=int(self.dt)))
        #             else:
        #                 logger.debug("Calibrating... {t}s".format(
        #                     t=self.dt))
        #
        #                 self.yaw0 = self.yaw
        #                 self.pitch0 = self.pitch
        #                 self.roll0 = self.roll
        #                 self.ax0 = self.ax
        #                 self.ay0 = self.ay
        #                 self.az0 = self.az
        #         else:
        #             self.t0 = time()
        #             yield (self.dt,
        #                    self.yaw,
        #                    self.ax,
        #                    self.ay)

        yield None, None, None, None
