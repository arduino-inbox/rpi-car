# coding=utf-8
"""
Generic node classes.
"""
import multiprocessing
import logging
from redis import StrictRedis
import time
from components.constants import *

logger = logging.getLogger()


class Node:
    """
    Base class for all nodes.
    """
    name = 'Generic Node'

    def __init__(self):
        logger.info("Initialized {name}".format(name=self.name))

    def do(self):
        """
        Do a bit of work.
        """
        raise NotImplementedError

    def run(self):
        """
        Node loop
        """
        while True:
            self.do()


#noinspection PyClassHasNoInit
class RedisConnectionFactory:
    """
    Redis connection factory.
    """
    @staticmethod
    def build():
        """
        Instantiate a redis connection

        @return: StrictRedis
        """
        # todo: provision connection properties
        return StrictRedis(host='localhost', port=6379, db=0)


class SubscriberNode(Node):
    """
    Pub/Sub subscriber node
    """
    def __init__(self, channels=None):
        Node.__init__(self)

        if not channels:
            channels = []
        if CHANNEL_ALL not in channels:
            channels.append(CHANNEL_ALL)

        self.redis_connection = RedisConnectionFactory.build()
        self.pub_sub = self.redis_connection.pubsub()
        self.pub_sub.subscribe(channels)
        logger.debug("{name} subscribed to {channels}.".format(name=self.name, channels=channels))
        self.data = {}

    def listen(self):
        """
        Listen to pub/sub messages and yield the updated data.

        @return: dict
        """
        for item in self.pub_sub.listen():
            self.data[item['channel']] = item['data']
            yield self.data

    def run(self):
        """
        Node loop.
        """
        while self.listen():
            self.do()


class PublisherNode(Node):
    """
    Pub/sub publisher node.
    """

    def __init__(self):
        Node.__init__(self)
        self.redis_connection = RedisConnectionFactory.build()

    def send(self, channel, message):
        """
        Send message.

        @param channel: string
        @param message: string
        """
        self.redis_connection.publish(channel, message)
        self.redis_connection.hset(str(timestamp()), channel, message)


class BrainNode(SubscriberNode, PublisherNode):
    """
    Dispatcher node.
    """
    name = 'Brain'

    def __init__(self):
        SubscriberNode.__init__(self, [
            'distance',
        ])
        PublisherNode.__init__(self)

        self.speed = 0
        self.direction = MOTOR_DIRECTION_STOP
        self.distance = DISTANCE_MAXIMUM
        self.data[CHANNEL_DISTANCE] = self.distance

    def do(self):
        """
        A bit of work.
        """
        self.distance = self.data[CHANNEL_DISTANCE]
        if self.distance < 50:
            self.speed = 0
            self.direction = MOTOR_DIRECTION_STOP
        else:
            self.speed += MOTOR_SPEED_STEP
            self.direction = MOTOR_DIRECTION_FORWARD
        self.send(CHANNEL_SPEED, self.speed)
        self.send(CHANNEL_DIRECTION, self.direction)


class ServoNode(SubscriberNode):
    """
    Generic servo motor node.
    """

    def __init__(self):
        SubscriberNode.__init__(self)
        # todo Implement
        raise NotImplementedError


class DistanceSensorNode(PublisherNode):
    """
    Generic distance sensor publisher node.
    """
    _distance = None

    def __init__(self):
        PublisherNode.__init__(self)
        self.set_distance(DISTANCE_MAXIMUM)

    def set_distance(self, distance):
        """
        Set and publish distance value.

        @param distance: float
        """
        self._distance = distance
        self.send(CHANNEL_DISTANCE, distance)


class NodeProcess(multiprocessing.Process):
    """
    System process running a node.
    """
    def __init__(self, node):
        multiprocessing.Process.__init__(self)
        self.node = node

    def run(self):
        """
        Start a node process.
        """
        logger.info("Node process running: {name}".format(name=self.node.name))
        self.node.run()

    def shutdown(self):
        """
        Terminate a node process.
        """
        self.terminate()
        logger.info("Node terminated: {name}".format(name=self.node.name))


#noinspection PyClassHasNoInit
class Car:
    """
    Main routine class
    """
    @staticmethod
    def run(nodes):
        """
        Main routine.

        @param nodes: list
        """
        start_time = timestamp()
        redis_connection = RedisConnectionFactory.build()
        redis_connection.publish(CHANNEL_ALL, 'Car started at {t}'.format(
            t=start_time))
        redis_connection.hset(start_time, 'start', 'OK')

        # start
        processes = []
        for node in nodes:
            p = NodeProcess(node)
            processes.append(p)
            p.start()

        # run
        time.sleep(1)

        # exit
        for p in processes:
            p.shutdown()

        stop_time = timestamp()
        redis_connection.publish(CHANNEL_ALL,
                                 'Car stopped at {t}'.format(t=stop_time))
        redis_connection.hset(stop_time, 'stop', 'OK')
        redis_connection.hset(stop_time, 'runtime', str(
            stop_time - start_time))

        # check stored data
        for key in redis_connection.keys():
            redis_connection.persist(str(key))
            data = redis_connection.hgetall(str(key))
            logger.debug("Redis data stored: " + key + " - " + str(data))


def timestamp():
    """
    Timestamp helper.
    @return: int
    """
    return int(round(time.time() * 10**9))
