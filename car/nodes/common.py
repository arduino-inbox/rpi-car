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
    name = 'Generic Node'

    def __init__(self):
        logger.info("Initialized {name}".format(name=self.name))

    def do(self):
        raise NotImplementedError


class RedisConnectionFactory:
    def __init__(self):
        pass

    @classmethod
    def build(cls):
        # todo: provision connection properties
        return StrictRedis(host='localhost', port=6379, db=0)


class Subscriber(Node):
    def __init__(self, channels=None):
        Node.__init__(self)

        if not channels:
            channels = []
        if CHANNEL_ALL not in channels:
            channels.append(CHANNEL_ALL)

        self.redis_connection = RedisConnectionFactory.build()
        self.pubsub = self.redis_connection.pubsub()
        self.pubsub.subscribe(channels)
        logger.debug("{name} subscribed to {channels}.".format(name=self.name, channels=channels))
        self.data = {}

    def listen(self):
        for item in self.pubsub.listen():
            self.data[item['channel']] = item['data']
            yield self.data

    def run(self):
        while self.listen():
            self.do()


def timestamp():
    return int(round(time.time() * 10**9))


class Publisher():
    def __init__(self):
        self.redis_connection = RedisConnectionFactory.build()

    def send(self, channel, message):
        self.redis_connection.publish(channel, message)
        self.redis_connection.hset(str(timestamp()), channel, message)


class BrainNode(Subscriber, Publisher):
    name = 'Brain'

    def __init__(self):
        Subscriber.__init__(self, [
            'distance',
        ])
        Publisher.__init__(self)

        self.speed = 0
        self.direction = MOTOR_DIRECTION_STOP
        self.distance = ULTRASONIC_MAX_DISTANCE
        self.data[CHANNEL_DISTANCE] = self.distance

    def do(self):
        self.distance = self.data[CHANNEL_DISTANCE]
        if self.distance < 50:
            self.speed = 0
            self.direction = MOTOR_DIRECTION_STOP
        else:
            self.speed += MOTOR_SPEED_STEP
            self.direction = MOTOR_DIRECTION_FORWARD
        self.send(CHANNEL_SPEED, self.speed)
        self.send(CHANNEL_DIRECTION, self.direction)


class ServoNode(Subscriber):
    #TODO: Implement
    pass


class DistanceSensor(Publisher):
    _distance = ULTRASONIC_MAX_DISTANCE

    def __init__(self):
        Publisher.__init__(self)
        self.set_distance(ULTRASONIC_MAX_DISTANCE)

    def set_distance(self, distance):
        # update
        self._distance = distance
        # notify
        self.send(CHANNEL_DISTANCE, distance)


class NodeProcess(multiprocessing.Process):
    def __init__(self, node):
        multiprocessing.Process.__init__(self)
        self.node = node

    def run(self):
        logger.info("Node process running: {name}".format(name=self.node.name))
        self.node.run()

    def shutdown(self):
        self.terminate()
        logger.info("Node terminated: {name}".format(name=self.node.name))


class Car:
    def __init__(self):
        pass

    @staticmethod
    def run(nodes):
        import time
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
