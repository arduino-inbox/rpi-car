# coding=utf-8
"""
Generic node classes.
"""
import multiprocessing


class Node:
    name = 'Generic Node'

    def __init__(self):
        print "Node Initialized.", self.name

    def do(self):
        raise NotImplemented


class ValueNode(Node):
    name = 'Car Node'
    value_proxy = None

    def __init__(self, value_proxy):
        Node.__init__(self)
        self.value_proxy = value_proxy

    def _get_value(self):
        return self.value_proxy.value

    def _set_value(self, value):
        self.value_proxy.value = value

    def do(self):
        print self.name, self.value_proxy.value


class ServoNode(ValueNode):
    #TODO: Implement
    pass


class DistanceSensorNode(ValueNode):
    def __init__(self, value_proxy):
        ValueNode.__init__(self, value_proxy)

    def get_distance(self):
        return self._get_value()

    def set_distance(self, distance):
        self._set_value(distance)


class MotorNode(ValueNode):

    FORWARD = 1
    STOP = 0
    BACKWARD = -1

    def __init__(self, direction, speed):
        ValueNode.__init__(self, value_proxy)

    def forward(self):
        self._set_value(self.FORWARD)

    def stop(self):
        self._set_value(self.STOP)

    def backward(self):
        self._set_value(self.BACKWARD)

    def get_direction(self):
        return self._get_value()


class NodeProcess(multiprocessing.Process):
    def __init__(self, node):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Value('i', 0, lock=False)
        self.node = node

    def run(self):
        while not self.exit.value == 1:
            self.node.do()

    def shutdown(self):
        print "Shutdown initiated", self.node.name
        self.exit.value = 1
