#! /usr/bin/python3

from Queue     import Queue
from threading import Lock


class Communicator:

    def __init__(self):
    
        self._queue = Queue
        self._lock  = Lock


    def write(self, *data):
    
        self._lock.acquire()
        for d in data:
            self._queue.put(d)
        self._lock.release()
        


    def read(self):
    
        r = []
    
        if self._queue.empty:
            return r
    
        self._lock.acquire()
        while not self._queue.empty:
            r.append(self._queue.get())
        self._lock.release()



class CommWriter:

    def __init__(self):
        pass
