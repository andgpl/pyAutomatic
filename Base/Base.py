#! /usr/bin/python3
import inspect
import operator

from Base.Comm  import Communicator, CommQueue




class Base(Communicator):

    def __init__(self, id_, desc):

        self.id   = id_
        self.name = self.__class__.__name__
        self.desc = desc
        
        # Write status information
        self._writer = None

        # Holds the child objects of this instance that are
        # also instances of Base in the order of their creation
        self._children = []

        for name, value in inspect.getmembers(self):

            if isinstance(value, Base):
                self._children.append(value)

        self._children.sort(key = operator.attrgetter("id"))


    def getInfo(self):
        from Info import Info
        return Info(self, [child.getInfo() for child in self._children])
        
        
    def run(self):
        pass



    #---- Communication ----
    def setWriter(self, writer):
        if isinstance(writer, CommQueue):
            self._writer = writer
            for child in self._children:
                child.setWriter(writer)


    def write(self, *data):
        if self._writer is not None:
            self._writer.write(*data)



if __name__ == "__main__":


    class Test(Base):
    
        x = Base(3, "a", "")      
        m = Base(1, "b", "")
        c = Base(2, "c", "")
        
        
        
    class TestA(Test):
    
        k = Base(0, "d", "")
        
    t = TestA(1000, "", "")
    print(list(map(lambda c: (c.id, c.name), t._children)))
