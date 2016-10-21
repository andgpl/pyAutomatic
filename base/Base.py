#! /usr/bin/python3
import inspect

from operator import attrgetter





class Base:

    def __init__(self, id_, desc):

        self.id   = id_
        self.name = self.__class__.__name__
        self.desc = desc


        # Holds the child objects of this instance that are
        # also instances of Base in the order of their creation
        self._children = []

        for name, value in inspect.getmembers(self):

            if isinstance(value, Base):
                self._children.append(value)

        self._children.sort(key = attrgetter("id"))




    def getInfo(self):
        from Info import Info
        return Info(self, [child.getInfo() for child in self._children])
        
        
    def run(self):
        pass



if __name__ == "__main__":


    class Test(Base):
    
        x = Base(3, "a", "")      
        m = Base(1, "b", "")
        c = Base(2, "c", "")
        
        
        
    class TestA(Test):
    
        k = Base(0, "d", "")
        
    t = TestA(1000, "", "")
    print(list(map(lambda c: (c.id, c.name), t._children)))
