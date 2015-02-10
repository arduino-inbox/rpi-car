# coding=utf-8
import math
import logging
import getopt
import sys

logger = logging.getLogger()


def convert_axes(qax, qay, qaz, pa, ra, yaw_control=False):
    """
    Axes: Convert the acceleration in g's to earth coordinates, then integrate to
    convert to speeds in earth's X and Y axes meters per second.

    Matrix 1: Uses X, Y, and Y accelerometers but omit yaw
    ---------
    |eax|   | cos(pitch),         0,          -sin(pitch)| |qax|
    |eay| = | 0,          cos(roll),           -sin(roll)| |qay|
    |eaz|   | sin(pitch), sin(roll), cos(pitch).cos(roll)| |qaz|

    Matrix 2: Uses X, Y, and Y accelerometers and include yaw (unsupported)
    ---------
    |eax|   | cos(pitch), sin(roll),          -sin(pitch)| |qax|
    |eay| = | sin(pitch), cos(roll),           -sin(roll)| |qay|
    |eaz|   | sin(pitch), sin(roll), cos(pitch).cos(roll)| |qaz|

    @param qax:
    @param qay:
    @param qaz:
    @param pa:
    @param ra:
    @param yaw_control: Boolean (Unused)
    @return:
    """
    if not yaw_control:
        eax = qax * math.cos(pa) - qaz * math.sin(pa)
        eay = qay * math.cos(ra) - qaz * math.sin(ra)
        eaz = qaz * math.cos(pa) * math.cos(ra) + qax * math.sin(pa) + qay * math.sin(ra) - 1.0

    else:
        eax = qax * math.cos(pa) + qay * math.sin(ra) - qaz * math.sin(pa)
        eay = qay * math.cos(ra) * qax * math.sin(pa) - qaz * math.sin(ra)
        eaz = qaz * math.cos(pa) * math.cos(ra) + qax * math.sin(pa) + qay * math.sin(ra) - 1.0

    return eax, eay, eaz


def check_cli(argv):
    """
    Check CLI validity, set calibrate_sensors / fly or sys.exit(1)

    @param argv:
    @return:
    """
    cli_fly = False
    cli_calibrate_sensors = False
    cli_video = False

    cli_hover_target = 680

    #-----------------------------------------------------------------------------------
    # Defaults for vertical velocity PIDs
    #-----------------------------------------------------------------------------------
    cli_vvp_gain = 300.0
    cli_vvi_gain = 150.0
    cli_vvd_gain = 0.0

    #-----------------------------------------------------------------------------------
    # Defaults for horizontal velocity PIDs
    #-----------------------------------------------------------------------------------
    cli_hvp_gain = 0.6
    cli_hvi_gain = 0.1
    cli_hvd_gain = 0.0

    #-----------------------------------------------------------------------------------
    # Defaults for absolute angle PIDs
    #-----------------------------------------------------------------------------------
    cli_aap_gain = 2.5
    cli_aai_gain = 0.0
    cli_aad_gain = 0.0

    #-----------------------------------------------------------------------------------
    # Defaults for rotation rate PIDs
    #-----------------------------------------------------------------------------------
    cli_rrp_gain = 150
    cli_rri_gain = 0.0
    cli_rrd_gain = 0.0

    #-----------------------------------------------------------------------------------
    # Other configuration defaults
    #-----------------------------------------------------------------------------------
    cli_test_case = 0
    cli_tau = 2.0        # 0.25 * 100 = 25 samples averaged for -3dB merge
    cli_dlpf = 5
    cli_loop_frequency = 500 # 100
    cli_matrix = 2
    cli_statistics = False
    cli_yaw_control = False
    cli_motion_frequency = 40
    cli_attitude_frequency = 40

    hover_target_defaulted = True
    no_drift_control = False
    rrp_set = False
    rri_set = False
    rrd_set = False
    aap_set = False
    aai_set = False
    aad_set = False

    #-----------------------------------------------------------------------------------
    # Right, let's get on with reading the command line and checking consistency
    #-----------------------------------------------------------------------------------
    try:
        opts, args = getopt.getopt(argv,'a:fcvh:l:m:nsy', ['tc=', 'vvp=', 'vvi=', 'vvd=', 'hvp=', 'hvi=', 'hvd=', 'aap=', 'aai=', 'aad=', 'arp=', 'ari=', 'ard=', 'tau=', 'dlpf='])
    except getopt.GetoptError:
        logger.critical('qcpi.py [-f][-h hover_target][-v][')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-f':
            cli_fly = True

        elif opt in '-h':
            cli_hover_target = int(arg)
            hover_target_defaulted = False

        elif opt in '-v':
            cli_video = True

        elif opt in '-a':
            cli_attitude_frequency = int(arg)

        elif opt in '-c':
            cli_calibrate_sensors = True

        elif opt in '-l':
            cli_loop_frequency = int(arg)

        elif opt in '-m':
            cli_motion_frequency = int(arg)

        elif opt in '-n':
            no_drift_control = True

        elif opt in '-s':
            cli_statistics = True

        elif opt in '-y':
            cli_yaw_control = True

        elif opt in '--vvp':
            cli_vvp_gain = float(arg)

        elif opt in '--vvi':
            cli_vvi_gain = float(arg)

        elif opt in '--vvd':
            cli_vvd_gain = float(arg)

        elif opt in '--hvp':
            cli_hvp_gain = float(arg)

        elif opt in '--hvi':
            cli_hvi_gain = float(arg)

        elif opt in '--hvd':
            cli_hvd_gain = float(arg)

        elif opt in '--aap':
            cli_aap_gain = float(arg)
            aap_set = True

        elif opt in '--aai':
            cli_aai_gain = float(arg)
            aai_set = True

        elif opt in '--aad':
            cli_aad_gain = float(arg)
            aad_set = True

        elif opt in '--arp':
            cli_rrp_gain = float(arg)
            rrp_set = True

        elif opt in '--ari':
            cli_rri_gain = float(arg)
            rri_set = True

        elif opt in '--ard':
            cli_rrd_gain = float(arg)
            rrd_set = True

        elif opt in '--tc':
            cli_test_case = int(arg)

        elif opt in '--tau':
            cli_tau = float(arg)

        elif opt in '--dlpf':
            cli_dlpf = int(arg)

    if not cli_calibrate_sensors and not cli_fly and cli_test_case == 0:
        logger.critical('Must specify one of -f or -c or --tc')
        logger.critical('  qcpi.py [-f] [-t speed] [-c] [-v]')
        logger.critical('  -f set whether to fly')
        logger.critical('  -h set the hover speed for manual testing')
        logger.critical('  -c calibrate sensors against temperature and save')
        logger.critical('  -s enable diagnostic statistics')
        logger.critical('  -n disable drift control')
        logger.critical('  -y enable yaw control (unsupported')
        logger.critical('  -v video the flight')
        logger.critical('  -l ??  set the processing loop frequency')
        logger.critical('  -a ??  set attitude PID update frequency')
        logger.critical('  -m ??  set motion PID update frequency')
        logger.critical('  --vvp  set vertical speed PID P gain')
        logger.critical('  --vvi  set vertical speed PID P gain')
        logger.critical('  --vvd  set vertical speed PID P gain')
        logger.critical('  --hvp  set horizontal speed PID P gain')
        logger.critical('  --hvi  set horizontal speed PID I gain')
        logger.critical('  --hvd  set horizontal speed PID D gain')
        logger.critical('  --aap  set absolute angle PID P gain')
        logger.critical('  --aai  set absolute angle PID I gain')
        logger.critical('  --aad  set absolute angle PID D gain')
        logger.critical('  --arp  set angular PID P gain')
        logger.critical('  --ari  set angular PID I gain')
        logger.critical('  --ari  set angular PID D gain')
        logger.critical('  --tc   select which testcase to run')
        logger.critical('  --tau  set the complementary filter period')
        logger.critical('  --dlpf set the digital low pass filter')
        sys.exit(2)

    elif not cli_calibrate_sensors and (cli_hover_target < 0 or cli_hover_target > 1000):
        logger.critical('Hover speed must lie in the following range')
        logger.critical('0 <= test speed <= 1000')
        sys.exit(2)

    elif cli_yaw_control:
        logger.critical('YAW control is not supported yet')
        sys.exit(2)

    elif cli_test_case == 0 and cli_fly:
        logger.critical('Pre-flight checks passed, enjoy your flight, sir!')
        if no_drift_control:
            cli_hvp_gain = 0.0
            cli_hvi_gain = 0.0
            cli_hvd_gain = 0.0
            cli_aap_gain = 1.5
            cli_aai_gain = 0.5
            cli_aad_gain = 0.01
            cli_rrp_gain = 110
            cli_rri_gain = 100
            cli_rrd_gain = 2.5

    elif cli_test_case == 0 and cli_calibrate_sensors:
        logger.critical('Calibrate sensors is it, sir!')

    elif cli_test_case == 0:
        logger.critical('You must specify flight (-f) or gravity calibration (-c)')
        sys.exit(2)

    elif cli_fly or cli_calibrate_sensors:
        logger.critical('Choose a specific test case (--tc) or fly (-f) or calibrate gravity (-g)')
        sys.exit(2)

    #---------------------------------------------------------------------------------------
    # Test case 1: Check all the blades work and spin in the right direction
    # Test case 2: Tune the rotational rate PIDs
    # Test case 3: Tune the absolute angle PIDs
    # Test case 4: Tune the hover speed
    #---------------------------------------------------------------------------------------

    elif cli_test_case < 1 or cli_test_case > 4:
        logger.critical('Select test case 1, 2, 3 or 4')
        sys.exit(2)

    elif hover_target_defaulted:
        logger.critical('You must choose a specific hover speed (-h) for all test cases.')
        sys.exit(2)

    elif cli_test_case == 2 and (not rrp_set or not rri_set or not rrd_set):
        logger.critical('You must choose a starting point for the angular rate PID P, I and D gains')
        logger.critical('Try sudo python ./qc.py --tc 2 -h 450 --arp 50 --ari 0.0 --ard 0.0 and work up from there')
        sys.exit(2)

    elif cli_test_case == 3 and (not aap_set or not aai_set or not aad_set):
        logger.critical('You must choose a starting point for the absolute angle PID P, I and D gains')
        logger.critical('Try sudo python ./qc.py --tc 3 -h 450 --aap 1.5 --aai 0.5 --aad 0.001 and work up from there')
        sys.exit(2)

    elif cli_test_case == 2:
        cli_vvp_gain = 0.0
        cli_vvi_gain = 0.0
        cli_vvd_gain = 0.0
        cli_hvp_gain = 0.0
        cli_hvi_gain = 0.0
        cli_hvd_gain = 0.0
        cli_aap_gain = 0.0
        cli_aai_gain = 0.0
        cli_aad_gain = 0.0

    elif cli_test_case == 3 or cli_test_case == 4:
        cli_vvp_gain = 0.0
        cli_vvi_gain = 0.0
        cli_vvd_gain = 0.0
        cli_hvp_gain = 0.0
        cli_hvi_gain = 0.0
        cli_hvd_gain = 0.0

    return cli_calibrate_sensors, cli_fly, cli_hover_target, cli_video, cli_vvp_gain, cli_vvi_gain, cli_vvd_gain, cli_hvp_gain, cli_hvi_gain, cli_hvd_gain, cli_aap_gain, cli_aai_gain, cli_aad_gain, cli_rrp_gain, cli_rri_gain, cli_rrd_gain, cli_test_case, cli_tau, cli_dlpf, cli_loop_frequency, cli_motion_frequency, cli_attitude_frequency, cli_statistics, cli_yaw_control