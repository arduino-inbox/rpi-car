# coding=utf-8
"""
Ultrasonic components.
"""
import logging
import os
import time
import math
import sys

logger = logging.getLogger()

from helpers import SmBusFactory
from qc import mpu6050, G_FORCE
from qc.utils import convert_axes, check_cli
from qc.pid import PID
from ..gpio import GpioComponent


class AccelerometerGyroscopeSensorComponent(GpioComponent):

    __CALIBRATION_ITERATIONS = 100

    if os.getenv('CALIBRATION_ITERATIONS'):
        try:
            ci = int(os.getenv('CALIBRATION_ITERATIONS'))
            if ci > __CALIBRATION_ITERATIONS:
                __CALIBRATION_ITERATIONS = ci
        except:
            pass


    delta_time = 0.0

    eax_average = 0.0
    eay_average = 0.0
    eaz_average = 0.0

    evx = 0.0
    evy = 0.0
    evz = 0.0

    evx_target = 0.0
    evy_target = 0.0
    evz_target = 0.0

    evz_out = 0.0

    pa_target = 0.0
    ra_target = 0.0
    ya_target = 0.0

    pr_out = 0.0
    rr_out = 0.0
    yr_out = 0.0

    update_start = 0.0
    hover_speed = 0
    vert_out = 0

    calibrate_sensors, flying, hover_target, shoot_video, vvp_gain, vvi_gain, vvd_gain, hvp_gain, hvi_gain, hvd_gain, aap_gain, aai_gain, aad_gain, rrp_gain, rri_gain, rrd_gain, test_case, tau, dlpf, loop_frequency, motion_frequency, attitude_frequency, statistics, yaw_control = check_cli(sys.argv[1:])

    #-------------------------------------------------------------------------------------------
    # The earth X axis speed controls forward / backward speed
    #-------------------------------------------------------------------------------------------
    PID_EVX_P_GAIN = hvp_gain
    PID_EVX_I_GAIN = hvi_gain
    PID_EVX_D_GAIN = hvd_gain

    #-------------------------------------------------------------------------------------------
    # The earth Y axis speed controls left / right speed
    #-------------------------------------------------------------------------------------------
    PID_EVY_P_GAIN = hvp_gain
    PID_EVY_I_GAIN = hvi_gain
    PID_EVY_D_GAIN = hvd_gain

    #-------------------------------------------------------------------------------------------
    # The earth Z axis speed controls rise / fall speed
    #-------------------------------------------------------------------------------------------
    PID_EVZ_P_GAIN = vvp_gain
    PID_EVZ_I_GAIN = vvi_gain
    PID_EVZ_D_GAIN = vvd_gain

    #-------------------------------------------------------------------------------------------
    # The PITCH ANGLE PID maintains a stable tilt angle about the Y-axis
    #-------------------------------------------------------------------------------------------
    PID_PA_P_GAIN = aap_gain
    PID_PA_I_GAIN = aai_gain
    PID_PA_D_GAIN = aad_gain

    #-------------------------------------------------------------------------------------------
    # The ROLL ANGLE PID maintains a stable tilt angle about the X-axis
    #-------------------------------------------------------------------------------------------
    PID_RA_P_GAIN = aap_gain
    PID_RA_I_GAIN = aai_gain
    PID_RA_D_GAIN = aad_gain

    #-------------------------------------------------------------------------------------------
    # The YAW ANGLE PID maintains a stable tilt angle about the Z-axis
    #-------------------------------------------------------------------------------------------
    PID_YA_P_GAIN = 0.0 # 2.5
    PID_YA_I_GAIN = 0.0 # 5.0
    PID_YA_D_GAIN = 0.0

    #-------------------------------------------------------------------------------------------
    # The PITCH RATE PID controls stable rotation rate around the Y-axis
    #-------------------------------------------------------------------------------------------
    PID_PR_P_GAIN = rrp_gain
    PID_PR_I_GAIN = rri_gain
    PID_PR_D_GAIN = rrd_gain

    #-------------------------------------------------------------------------------------------
    # The ROLL RATE PID controls stable rotation rate around the X-axis
    #-------------------------------------------------------------------------------------------
    PID_RR_P_GAIN = rrp_gain
    PID_RR_I_GAIN = rri_gain
    PID_RR_D_GAIN = rrd_gain

    #-------------------------------------------------------------------------------------------
    # The YAW RATE PID controls stable rotation speed around the Z-axis
    #-------------------------------------------------------------------------------------------
    PID_YR_P_GAIN = 0 # rrp_gain / 2.5
    PID_YR_I_GAIN = 0 # rri_gain / 2.5
    PID_YR_D_GAIN = 0 # rrd_gain / 2.5


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
        self.qax_average = 0.0
        self.qay_average = 0.0
        self.qaz_average = 0.0
        for self.loop_count in range(0, 50, 1):
            self.qax, self.qay, self.qaz, self.qgx, self.qgy, self.qgz = self.mpu.readSensors()
            self.qax_average += self.qax
            self.qay_average += self.qay
            self.qaz_average += self.qaz
            time.sleep(0.05)
        self.qax = self.qax_average / 50.0
        self.qay = self.qay_average / 50.0
        self.qaz = self.qaz_average / 50.0

        self.prev_c_pitch, self.prev_c_roll, prev_c_tilt  = self.mpu.getEulerAngles(self.qax, self.qay, self.qaz)
        logger.critical("Platform tilt: pitch %f, roll %f", self.prev_c_pitch * 180 / math.pi, self.prev_c_roll * 180 / math.pi)

        #-------------------------------------------------------------------------------------------
        # Prime the earth axis accelerometer values for accurate earth axis speed integration
        #-------------------------------------------------------------------------------------------
        self.eax, self.eay, self.eaz = convert_axes(self.qax, self.qay, self.qaz, self.prev_c_pitch, self.prev_c_roll)
        self.eax_offset = self.eax
        self.eay_offset = self.eay
        self.eaz_offset = self.eaz

        logger.critical("Platform motion: qax %f, qay %f, qaz %f, g %f", self.qax, self.qay, self.qaz, math.pow(math.pow(self.qax, 2) + math.pow(self.qay, 2) + math.pow(self.qaz, 2), 0.5))
        logger.critical("Platform motion: eax %f, eay %f, eaz %f, g %f", self.eax, self.eay, self.eaz, math.pow(math.pow(self.eax, 2) + math.pow(self.eay, 2) + math.pow(1.0 + self.eaz, 2), 0.5))

        #-------------------------------------------------------------------------------------------
        # Preset the integrated gyro to match the take-off angle
        #-------------------------------------------------------------------------------------------
        self.i_pitch = self.prev_c_pitch
        self.i_roll = self.prev_c_roll
        self.i_yaw = 0.0

        time.sleep(2.0)

        #------------------------------------------------------------------------------------------
        # Set up the bits of state setup before takeoff
        #-------------------------------------------------------------------------------------------

        self.time_handling_sensors = 0.0
        self.time_handling_eangles = 0.0
        self.time_handling_iangles = 0.0
        self.time_handling_angles_filter = 0.0
        self.time_handling_axes_shift = 0.0
        self.time_handling_motion_pids = 0.0
        self.time_handling_attitude_pids = 0.0
        self.time_handling_pid_outputs = 0.0
        self.time_handling_diagnostics = 0.0
        self.time_handling_sleep = 0.0

        ############################################################################################
        # Enable time dependent factors PIDs - everything beyond here and "while self.keep_looping:" is time
        # critical and should be kept to an absolute minimum.
        ############################################################################################


        #-------------------------------------------------------------------------------------------
        # Start the pitch, roll and yaw angle PIDs
        #-------------------------------------------------------------------------------------------
        self.pa_pid = PID(self.PID_PA_P_GAIN, self.PID_PA_I_GAIN, self.PID_PA_D_GAIN)
        self.ra_pid = PID(self.PID_RA_P_GAIN, self.PID_RA_I_GAIN, self.PID_RA_D_GAIN)
        self.ya_pid = PID(self.PID_YA_P_GAIN, self.PID_YA_I_GAIN, self.PID_YA_D_GAIN)

        #-------------------------------------------------------------------------------------------
        # Start the pitch, roll and yaw rate PIDs
        #-------------------------------------------------------------------------------------------
        self.pr_pid = PID(self.PID_PR_P_GAIN, self.PID_PR_I_GAIN, self.PID_PR_D_GAIN)
        self.rr_pid = PID(self.PID_RR_P_GAIN, self.PID_RR_I_GAIN, self.PID_RR_D_GAIN)
        self.yr_pid = PID(self.PID_YR_P_GAIN, self.PID_YR_I_GAIN, self.PID_YR_D_GAIN)

        #-------------------------------------------------------------------------------------------
        # Start the X, Y (horizontal) and Z (vertical) velocity PIDs
        #-------------------------------------------------------------------------------------------
        self.evx_pid = PID(self.PID_EVX_P_GAIN, self.PID_EVX_I_GAIN, self.PID_EVX_D_GAIN)
        self.evy_pid = PID(self.PID_EVY_P_GAIN, self.PID_EVY_I_GAIN, self.PID_EVY_D_GAIN)
        self.evz_pid = PID(self.PID_EVZ_P_GAIN, self.PID_EVZ_I_GAIN, self.PID_EVZ_D_GAIN)

        self.rtf_time = 0.0
        self.elapsed_time = 0.0
        self.start_time = time.time()
        self.last_log_time = self.start_time
        self.current_time = self.start_time
        self.prev_sample_time = self.current_time
        self.last_motion_update = self.current_time
        self.last_attitude_update = self.current_time
        self.update_PWM = False
        self.ea_averaging_start = self.current_time
        self.loop_count = 0

    def reading(self):
        #-----------------------------------------------------------------------------------
        # Update the elapsed time since start, the time for the last iteration, and
        # set the next sleep time to compensate for any overrun in scheduling.
        #-----------------------------------------------------------------------------------
        self.current_time = time.time()
        self.delta_time = self.current_time - self.start_time - self.elapsed_time
        self.elapsed_time = self.current_time - self.start_time
        self.loop_count += 1

        #===================================================================================
        # Inputs: Read the data from the accelerometer and gyro
        #===================================================================================
        self.qax, self.qay, self.qaz, self.qgx, self.qgy, self.qgz = self.mpu.readSensors()

        #===================================================================================
        # Angles: Get the Euler angles in radians
        #===================================================================================
        self.e_pitch, self.e_roll, self.e_tilt  = self.mpu.getEulerAngles(self.qax, self.qay, self.qaz)

        #-----------------------------------------------------------------------------------
        # Integrate the gyros angular velocity to determine absolute angle of tilt in radians
        # Note that this is for diagnostic purposes only.
        #-----------------------------------------------------------------------------------
        self.i_pitch += self.qgy * self.delta_time
        self.i_roll += self.qgx * self.delta_time
        self.i_yaw += self.qgz * self.delta_time

        #===================================================================================
        # Filter: Apply complementary filter to ensure long-term accuracy of pitch / roll angles
        # 1/self.tau is the handover frequency that the integrated gyro high pass filter is taken over
        # by the accelerometer Euler low-pass filter providing fast reaction to change from the
        # gyro yet with low noise accurate Euler angles from the acclerometer.
        #
        # The combination of self.tau plus the time increment (delta_time) provides a fraction to mix
        # the two angles sources.
        #===================================================================================
        self.tau_fraction = self.tau / (self.tau + self.delta_time)

        self.c_pitch = self.tau_fraction * (self.prev_c_pitch + self.qgy * self.delta_time) + (1 - self.tau_fraction) * self.e_pitch
        self.prev_c_pitch = self.c_pitch

        self.c_roll = self.tau_fraction * (self.prev_c_roll + self.qgx * self.delta_time) + (1 - self.tau_fraction) * self.e_roll
        self.prev_c_roll = self.c_roll

        #-----------------------------------------------------------------------------------
        # Choose the best measure of the angles
        #-----------------------------------------------------------------------------------
        self.pa = self.c_pitch
        self.ra = self.c_roll
        self.ya = self.i_yaw

        #-----------------------------------------------------------------------------------
        # Convert quad orientated axes accelerometer reading to earth orientated axes
        #-----------------------------------------------------------------------------------
        self.eax, self.eay, self.eaz = convert_axes(self.qax, self.qay, self.qaz, self.c_pitch, self.c_roll)

        #-----------------------------------------------------------------------------------
        # Integrate to earth axes' velocities
        #-----------------------------------------------------------------------------------
        self.evx += (self.eax - self.eax_offset) * self.delta_time * G_FORCE
        self.evy += (self.eay - self.eay_offset) * self.delta_time * G_FORCE
        self.evz += (self.eaz - self.eaz_offset) * self.delta_time * G_FORCE

        #-----------------------------------------------------------------------------------
        # Integrate out the accelerometer noise across the time between motion PID updates
        #-----------------------------------------------------------------------------------
        self.eax_average += (self.eax - self.eax_offset) * self.delta_time
        self.eay_average += (self.eay - self.eay_offset) * self.delta_time
        self.eaz_average += (self.eaz - self.eaz_offset) * self.delta_time

        #-----------------------------------------------------------------------------------
        # Diagnostic statistics log - every 0.1s
        #-----------------------------------------------------------------------------------
        logger.debug("{et}, {dt}, {l}, {ya}, {ax}, {ay}, {vx}, {vy}".format(
            et=self.elapsed_time,
            dt=self.delta_time,
            l=self.loop_count,
            ya=self.ya,
            ax=self.eax_average,
            ay=self.eay_average,
            vx=self.evx,
            vy=self.evy
        ))

        #-----------------------------------------------------------------------------------
        # Slow down the scheduling loop to avoid making accelerometer noise.  This sleep critically
        # takes place between the update of the PWM and reading the sensors, so that any
        # PWM changes can stabilize (i.e. spikes reacted to) prior to reading the sensors.
        #-----------------------------------------------------------------------------------
        self.loop_time = time.time() - self.current_time
        self.sleep_time = 1 / self.loop_frequency - self.loop_time
        if self.sleep_time < 0.0:
            self.sleep_time = 0.0
        time.sleep(self.sleep_time)


        #-------------------------------------------------------------------------------------------
        # Dump the loops per second
        #-------------------------------------------------------------------------------------------
        # logger.debug("loop speed %f loops per second", self.loop_count / self.elapsed_time)

        # DT, Yaw, Acc, Vel, Dist
        return self.delta_time, self.ya, 0.0, 0.0, 0.0

