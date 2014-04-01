# coding=utf-8
"""
Main module
"""

import redis
import threading


class Subscriber(threading.Thread):
    def __init__(self, channels):
        threading.Thread.__init__(self)
        self.redis = redis.Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)


    def work(self, item):
        print item['channel'], ":", item['data']

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                self.work(item)


class Publisher():
    def __init__(self, channel):
        self.redis = redis.Redis()
        self.channel = channel

    def send(self, message):
        self.redis.publish(self.channel, message)
