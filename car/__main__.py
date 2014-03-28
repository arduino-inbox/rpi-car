# coding=utf-8
"""
Main executable of python robot car.
"""
import multiprocessing
import time

from nodes import MotorDriverNode, UltrasonicSensorNode, BrainNode, NodeProcess
from ctypes import c_int, c_float

import dbus
#from dbus.mainloop.glib import DBusGMainLoop
from dbus import service


class Example(dbus.service.Object):
    def __init__(self, path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), path)

    @dbus.service.signal(dbus_interface='com.example.Sample',
                         signature='us')
    def NumberOfBottlesChanged(self, number, contents):
        print "%d bottles of %s on the wall" % (number, contents)

e = Example('/bottle-counter')
e.NumberOfBottlesChanged(100, 'beer')

#dbus_loop = DBusGMainLoop()
#bus = dbus.SessionBus(mainloop=dbus_loop)
#
#
#distance = multiprocessing.Value(c_float, 0, lock=False)
#distance_sensor = UltrasonicSensorNode(value_proxy=distance)
#
#motor_value_proxy = multiprocessing.Value(c_int, 0, lock=False)
#motor = MotorDriverNode(value_proxy=motor_value_proxy)
#
#brain = BrainNode(distance=distance, mvp=motor_value_proxy)
#
#nodes = [
#    motor,
#    distance_sensor,
#    brain,
#]
#
#processes = []
#for node in nodes:
#    p = NodeProcess(node)
#    processes.append(p)
#    p.start()
#
## exit
#time.sleep(30)
#for p in processes:
#    p.shutdown()
#
