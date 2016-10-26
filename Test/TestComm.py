#! /usr/bin/python3

from Base.Comm          import CommQueue
from Test.EventAnalyser import EventAnalyser



class TestCommQueue(CommQueue):


    def __init__(self):
        super(TestCommQueue, self).__init__(self)

        self._analyser = EventAnalyser()


    def write(self, *data)

        for d in data:

            super(TestCommQueue, self).write(d)

            anaEvents = self._analyser.analyse(d)
            if len(aEvents):
                super(TestCommQueue, self).write(*anaEvents)

            
            
