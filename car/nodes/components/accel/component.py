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

    evx_diags = "0.0, 0.0, 0.0"
    evy_diags = "0.0, 0.0, 0.0"
    evz_diags = "0.0, 0.0, 0.0"
    pa_diags = "0.0, 0.0, 0.0"
    ra_diags = "0.0, 0.0, 0.0"
    ya_diags = "0.0, 0.0, 0.0"
    pr_diags = "0.0, 0.0, 0.0"
    rr_diags = "0.0, 0.0, 0.0"
    yr_diags = "0.0, 0.0, 0.0"

    update_start = 0.0
    hover_speed = 0
    vert_out = 0

    calibrate_sensors, flying, hover_target, shoot_video, vvp_gain, vvi_gain, vvd_gain, hvp_gain, hvi_gain, hvd_gain, aap_gain, aai_gain, aad_gain, rrp_gain, rri_gain, rrd_gain, test_case, tau, dlpf, loop_frequency, motion_frequency, attitude_frequency, statistics, yaw_control = check_cli(sys.argv[1:])
    logger.debug("calibrate_sensors = %s, fly = %s, hover_target = %d, shoot_video = %s, vvp_gain = %f, vvi_gain = %f, vvd_gain= %f, hvp_gain = %f, hvi_gain = %f, hvd_gain = %f, aap_gain = %f, aai_gain = %f, aad_gain = %f, rrp_gain = %f, rri_gain = %f, rrd_gain = %f, test_case = %d, tau = %f, dlpf = %d, loop_frequency = %d, motion_frequency = %d, attitude_frequency = %d, statistics = %s, yaw_control = %d", calibrate_sensors, flying, hover_target, shoot_video, vvp_gain, vvi_gain, vvd_gain, hvp_gain, hvi_gain, hvd_gain, aap_gain, aai_gain, aad_gain, rrp_gain, rri_gain, rrd_gain, test_case, tau, dlpf, loop_frequency, motion_frequency, attitude_frequency, statistics, yaw_control)


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

        #-----------------------------------------------------------------------------------
        # Track proportion of time handling sensors
        #-----------------------------------------------------------------------------------
        self.sample_time = time.time()
        self.time_handling_sensors += self.sample_time - self.prev_sample_time
        self.prev_sample_time = self.sample_time

        #===================================================================================
        # Angles: Get the Euler angles in radians
        #===================================================================================
        self.e_pitch, self.e_roll, self.e_tilt  = self.mpu.getEulerAngles(self.qax, self.qay, self.qaz)

        #-----------------------------------------------------------------------------------
        # Track proportion of time handling euler angles
        #-----------------------------------------------------------------------------------
        self.sample_time = time.time()
        self.time_handling_eangles += self.sample_time - self.prev_sample_time
        self.prev_sample_time = self.sample_time

        #-----------------------------------------------------------------------------------
        # Integrate the gyros angular velocity to determine absolute angle of tilt in radians
        # Note that this is for diagnostic purposes only.
        #-----------------------------------------------------------------------------------
        self.i_pitch += self.qgy * self.delta_time
        self.i_roll += self.qgx * self.delta_time
        self.i_yaw += self.qgz * self.delta_time

        #-----------------------------------------------------------------------------------
        # Track proportion of time handling integrated angles
        #-----------------------------------------------------------------------------------
        self.sample_time = time.time()
        self.time_handling_iangles += self.sample_time - self.prev_sample_time
        self.prev_sample_time = self.sample_time

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
        # Track proportion of time handling angle filter
        #-----------------------------------------------------------------------------------
        sample_time = time.time()
        self.time_handling_angles_filter += sample_time - self.prev_sample_time
        self.prev_sample_time = sample_time

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
        # Track proportion of time handling sensor angles
        #-----------------------------------------------------------------------------------
        sample_time = time.time()
        self.time_handling_axes_shift += sample_time - self.prev_sample_time
        self.prev_sample_time = sample_time

        #-----------------------------------------------------------------------------------
        # The attitude PID targets are updated with new motion PID outputs at 31Hz.
        # The attitude PID outputs are updated every 100Hz.
        #-----------------------------------------------------------------------------------
        if self.current_time - self.last_motion_update >= 1/self.motion_frequency:
            self.last_motion_update -= self.current_time

            #===========================================================================
            # Motion PIDs: Run the horizontal speed PIDs each rotation axis to determine
            # targets for absolute angle PIDs and the verical speed PID to control height.
            #===========================================================================
            [p_out, i_out, d_out] = self.evx_pid.Compute(self.evx, self.evx_target)
            self.evx_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            self.evx_out = p_out + i_out + d_out

            [p_out, i_out, d_out] = self.evy_pid.Compute(self.evy, self.evy_target)
            self.evy_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            self.evy_out =  p_out + i_out + d_out

            [p_out, i_out, d_out] = self.evz_pid.Compute(self.evz, self.evz_target)
            self.evz_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            self.evz_out = p_out + i_out + d_out

            #---------------------------------------------------------------------------
            # Work out the earth axis acceleration averages
            #---------------------------------------------------------------------------
            self.eax_average /= (self.current_time - self.ea_averaging_start)
            self.eay_average /= (self.current_time - self.ea_averaging_start)
            self.eaz_average /= (self.current_time - self.ea_averaging_start)

            #---------------------------------------------------------------------------
            # Convert the horizontal velocity PID output i.e. the horizontal acceleration
            # target in q's into the pitch and roll angle PID targets in radians
            #---------------------------------------------------------------------------
            self.pa_target = -math.atan2(self.evx_out, 1.0 + self.eaz_average)
            self.ra_target = -math.atan2(self.evy_out, 1.0 + self.eaz_average)

            #---------------------------------------------------------------------------
            # Restart integrating out accelerometer noise
            #---------------------------------------------------------------------------
            self.ea_averaging_start = self.current_time
            self.eax_average = 0.0
            self.eay_average = 0.0
            self.eaz_average = 0.0

            #---------------------------------------------------------------------------
            # Convert the vertical velocity PID output direct to PWM pulse width.
            #---------------------------------------------------------------------------
            self.vert_out = self.hover_speed + int(round(self.evz_out))

            #---------------------------------------------------------------------------
            # Track proportion of time handling speed PIDs
            #---------------------------------------------------------------------------
            sample_time = time.time()
            self.time_handling_motion_pids += sample_time - self.prev_sample_time
            self.prev_sample_time = sample_time


        if self.current_time - self.last_attitude_update >= 1/self.attitude_frequency:
            self.last_attitude_update -= self.current_time

            #===========================================================================
            # Attitude PIDs: Run the absolute and and rotoation rate PIDs each rotation
            # axis to determine overall PWM output.
            #===========================================================================
            [p_out, i_out, d_out] = self.pa_pid.Compute(self.pa, self.pa_target)
            self.pa_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            pr_target = p_out + i_out + d_out
            [p_out, i_out, d_out] = self.ra_pid.Compute(self.ra, self.ra_target)
            self.ra_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            rr_target = p_out + i_out + d_out
            [p_out, i_out, d_out] = self.ya_pid.Compute(self.ya, self.ya_target)
            self.ya_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            yr_target = p_out + i_out + d_out

            [p_out, i_out, d_out] = self.pr_pid.Compute(self.qgy, pr_target)
            self.pr_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            self.pr_out = p_out + i_out + d_out
            [p_out, i_out, d_out] = self.rr_pid.Compute(self.qgx, rr_target)
            self.rr_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            self.rr_out = p_out + i_out + d_out
            [p_out, i_out, d_out] = self.yr_pid.Compute(self.qgz, yr_target)
            self.yr_diags = "%f, %f, %f" % (p_out, i_out, d_out)
            self.yr_out = p_out + i_out + d_out

            #---------------------------------------------------------------------------
            # Convert the rotation rate PID outputs direct to PWM pulse width
            #---------------------------------------------------------------------------
            self.pr_out = int(round(self.pr_out / 2))
            self.rr_out = int(round(self.rr_out / 2))
            self.yr_out = int(round(self.yr_out / 2))

            #---------------------------------------------------------------------------
            # Track proportion of time handling angle PIDs
            #---------------------------------------------------------------------------
            sample_time = time.time()
            self.time_handling_attitude_pids += sample_time - self.prev_sample_time
            self.prev_sample_time = sample_time

        #-----------------------------------------------------------------------------------
        # Diagnostic statistics log - every 0.1s
        #-----------------------------------------------------------------------------------
        logger.debug('Time, DT, Loop, evz_target, qgx, qgy, qgz, qax, qay, qaz, eax, eay, eaz, evx, evy, evz, i pitch, i roll, e pitch, e roll, c pitch, c roll, i yaw, e tilt, exp, exi, exd, pa_target, pap, pai, pad, prp, pri, prd, pr_out, eyp, eyi, eyd, ra_target, rap, rai, rad, rrp, rri, rrd, rr_out, ezp, ezi, ezd, evz_out, yap, yai, yap, yrp, yri, yrd, yr_out, FL spin, FR spin, BL spin, BR spin')
        logger.debug("{et}, {dt}, {l}, {ya}, {ax}, {ay}".format(
            et=self.elapsed_time,
            dt=self.delta_time,
            l=self.loop_count,
            ya=self.i_yaw,
            ax=self.eax,
            ay=self.eay
        ))

        # logger.debug('Time, DT, Loop, evz_target, qgx, qgy, qgz, qax, qay, qaz, eax, eay, eaz, evx, evy, evz, i pitch, i roll, e pitch, e roll, c pitch, c roll, i yaw, e tilt, exp, exi, exd, pa_target, pap, pai, pad, prp, pri, prd, pr_out, eyp, eyi, eyd, ra_target, rap, rai, rad, rrp, rri, rrd, rr_out, ezp, ezi, ezd, evz_out, yap, yai, yap, yrp, yri, yrd, yr_out, FL spin, FR spin, BL spin, BR spin')
        #'0.075547, 0.075547, 1, 0.000000, -0.000194, 0.000217, 0.000232, -0.034452, -0.031382, 0.900066, -0.001923, -0.000822, -0.098730, -0.001425, -0.000609, 0.000529, -2.065121, -1.942578, -2.192070, -1.996880, -2.069741, -1.944554, 0.001003, 2.963938, 0.000855, 0.000014, 0.000000, -0.000868, 0.088140, 0.000000, 0.000000, 13.188448, 0.000000, 0.000000, 7.000000, 0.000366, 0.000006, 0.000000, -0.000371, 0.083919, 0.000000, 0.000000, 12.617054, 0.000000, 0.000000, 6.000000, -0.158810, -0.007599, -0.000000, -0.166409, -0.000000, -0.000000, -0.000000, -0.000000, -0.000000, -0.000000, 0.000000'
        # logger.debug(
        #     '%f, %f, %d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %s, %f, %s, %s, %f, %s, %f, %s, %s, %f, %s, %f, %s, %s, %f',
        #     self.elapsed_time, self.delta_time, self.loop_count, self.evz_target, self.qgx, self.qgy, self.qgz,
        #     self.qax, self.qay, self.qaz, self.eax, self.eay,
        #     self.eaz, self.evx, self.evy, self.evz, math.degrees(self.i_pitch), math.degrees(self.i_roll),
        #     math.degrees(self.e_pitch),
        #     math.degrees(self.e_roll), math.degrees(self.c_pitch), math.degrees(self.c_roll), math.degrees(self.i_yaw),
        #     math.degrees(self.e_tilt), self.evx_diags, self.pa_target, self.pa_diags, self.pr_diags, self.pr_out,
        #     self.evy_diags, self.ra_target, self.ra_diags, self.rr_diags, self.rr_out, self.evz_diags, self.evz_out,
        #     self.ya_diags, self.yr_diags, self.yr_out)

        #-----------------------------------------------------------------------------------
        # Track proportion of time logging diagnostics
        #-----------------------------------------------------------------------------------
        self.sample_time = time.time()
        self.time_handling_diagnostics += self.sample_time - self.prev_sample_time
        self.prev_sample_time = self.sample_time

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

        #-----------------------------------------------------------------------------------
        # Track proportion of time sleeping
        #-----------------------------------------------------------------------------------
        self.sample_time = time.time()
        self.time_handling_sleep += self.sample_time - self.prev_sample_time
        self.prev_sample_time = self.sample_time

        #-------------------------------------------------------------------------------------------
        # Dump the loops per second
        #-------------------------------------------------------------------------------------------
        logger.debug("loop speed %f loops per second", self.loop_count / self.elapsed_time)

        # #-------------------------------------------------------------------------------------------
        # # Dump the percentage time handling each step
        # #-------------------------------------------------------------------------------------------
        # logger.critical("%% sensors:          %f", self.time_handling_sensors / self.elapsed_time * 100.0)
        # logger.critical("%% eangles:          %f", self.time_handling_eangles / self.elapsed_time * 100.0)
        # logger.critical("%% iangles:          %f", self.time_handling_iangles / self.elapsed_time * 100.0)
        # logger.critical("%% angles_filter:    %f", self.time_handling_angles_filter / self.elapsed_time * 100.0)
        # logger.critical("%% axes_shift:       %f", self.time_handling_axes_shift / self.elapsed_time * 100.0)
        # logger.critical("%% motion_pids:      %f", self.time_handling_motion_pids / self.elapsed_time * 100.0)
        # logger.critical("%% attitude_pids:    %f", self.time_handling_attitude_pids / self.elapsed_time * 100.0)
        # logger.critical("%% pid_outputs:      %f", self.time_handling_pid_outputs / self.elapsed_time * 100.0)
        # logger.critical("%% pid_diagnosticss: %f", self.time_handling_diagnostics / self.elapsed_time * 100.0)
        # logger.critical("%% sleep:            %f", self.time_handling_sleep / self.elapsed_time * 100.0)
        #
        mpu6050_misses, i2c_misses = self.mpu.getMisses()
        logger.debug("mpu6050 %d misses, i2c %d misses", mpu6050_misses, i2c_misses)

        return self.delta_time, self.ya, self.eax, self.eay

