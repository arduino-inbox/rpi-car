# coding=utf-8
"""
Pubsub module
"""

import redis


class Subscriber():
    def __init__(self, channels):
        self.redis = redis.Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def listen(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                print item['channel'], ":", item['data']


class Publisher():
    def __init__(self, channel):
        self.redis = redis.Redis()
        self.channel = channel

    def send(self, message):
        self.redis.publish(self.channel, message)
