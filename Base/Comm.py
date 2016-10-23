#! /usr/bin/python3
from abc        import ABCMeta, abstractmethod
from queue      import Queue
from threading  import Lock



class Communicator(metaclass=ABCMeta):

    @abstractmethod
    def write(self, *data):
        pass


    @abstractmethod
    def read(self):
        return []


    @abstractmethod
    def setWriter(self, writer):
        pass


    @abstractmethod
    def setReader(self, reader):
        pass




class CommQueue:

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
