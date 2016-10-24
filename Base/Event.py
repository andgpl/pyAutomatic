#! /usr/bin/python3
import time

from Base.EventType import EventType



class Event:

    def __init__(self, type_, mesg):

        if not isinstance(type_, EventType):
            #TODO: raise exception
            return
    
        if not isinstance(mesg, str):
            #TODO: raise exception
            return

        self.type    = type_
        self.message = mesg
        self.time    = time.time()
        
        
    def __str__(self):
        return "{} : {}".format(self.type.name, self.message)
        
        
        
if __name__ == "__main__":

    e = Event(EventType.LOG, "log this!")
    print(e)
