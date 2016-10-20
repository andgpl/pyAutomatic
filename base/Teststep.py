#! /usr/bin/python3
import inspect

from Base       import Base
from Decorator  import Decorator


@Decorator.createDecorator
class Teststep(Base):



    def __init__(self, _id, desc=""):

        print(self.__class__.__name__)
        print(super(Teststep, self))
        super(Teststep, self).__init__(_id, desc)


        # Function to be executed when run method is called
        if hasattr(self, self.name) and\
                                inspect.ismethod(getattr(self, self.name)):
            self._stepFn = getattr(self, self.name)
        else:
            self._stepFn = None


    def run(self):

        if self._stepFn is None:
            return

        self._stepFn()






if __name__ == "__main__":

    print(Teststep)

    @Teststep
    def doSomething(self):
        print(self.id,':',self.desc)



    #doSomething.run()

    #print(doSomething.getInfo())
