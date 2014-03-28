# coding=utf-8
from multiprocessing import Process, Queue, Lock
import random


def f(q, x, l):
    try:
        while True:
            m = q.get()
            if m[0] == x:
                l.acquire()
                print x, m[1]
                l.release()
                if m[1] == 'exit':
                    return
    except Exception, e:
        print e.message
        return


if __name__ == '__main__':
    ps = []
    q = Queue()
    lock = Lock()

    try:
        for x in xrange(1, 10):
            p = Process(target=f, args=(q, x, lock))
            p.start()
            ps.append(p)
        while True:
            q.put([random.randint(1, 9), random.random()])

    except KeyboardInterrupt:
        for x in xrange(1, 10):
            q.put([x, 'exit'])
        for p in ps:
            p.join()
            p.terminate()

        q.close()
        exit(1)