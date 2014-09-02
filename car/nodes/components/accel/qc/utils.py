# coding=utf-8
import math

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
