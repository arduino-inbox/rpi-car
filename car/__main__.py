# coding=utf-8
"""
Main executable of python robot car.
"""
from nodes.pubsub import Subscriber, Publisher

s = Subscriber(['test1', 'test2'])
s.start()

p1 = Publisher('test1')
p1.send('P1 says hi.')
p1.send('P1 says unsubscribe.')

p2 = Publisher('test2')
p2.send('P2 says hi.')
p2.send('P2 says unsubscribe.')
p2.send('KILL')


#import multiprocessing
#import time
#
#from nodes import MotorDriverNode, UltrasonicSensorNode, BrainNode, NodeProcess
#from ctypes import c_int, c_float
#
#
#
#
#distance = multiprocessing.Value(c_float, 0, lock=False)
#distance_sensor = UltrasonicSensorNode(value_proxy=distance)
#
##motor_value_proxy = multiprocessing.Value(c_int, 0, lock=False)
##motor = MotorDriverNode(value_proxy=motor_value_proxy)
##
##brain = BrainNode(
##    distance=distance,
##    direction=direction,
##    speed=speed,
##    turn=turn)
#
#nodes = [
#    #motor,
#    distance_sensor,
#    #brain,
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
