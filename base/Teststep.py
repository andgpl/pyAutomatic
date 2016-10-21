#! /usr/bin/python3
import inspect

from Base      import Base
from Decorator import Decorator



TS_INSTANCE_ARGUMENT = '_teststep_'


@Decorator.createDecorator
class Teststep(Base):



    def __init__(self, _id, desc=""):

        # The Teststep class has been wrapped by the decorator.
        # The original class can still be found by accessing
        # __DecoBaseClass__.
        super(Teststep.__DecoBaseClass__, self).__init__(_id, desc)


        # Function to be executed when run method is called
        if hasattr(self, self.name) and\
                                inspect.isfunction(getattr(self, self.name)):
            self._stepFn = getattr(self, self.name)
        else:
            self._stepFn = None
            return

        # Teststep function can get information about its teststep instance
        # at runtime when it has the special argument TS_INSTANCE_ARGUMENT.
        # The TS_INSTANCE_ARGUMENT must be the last positional argument.

        self._posArgs = []
        sig = inspect.Signature.from_callable(self._stepFn)
        for paramName, paramType in sig.parameters.items():
            if paramType.default == paramType.empty:
                self._posArgs.append(paramName)

        self._addStepInfoArg = (len(self._posArgs) > 0) and\
                                     (self._posArgs[-1] == TS_INSTANCE_ARGUMENT)


    def run(self, *args):

        if self._stepFn is None:
            return


        if self._addStepInfoArg:
            args += (self,)

        self._stepFn(*args)



    def __call__(self, *args, **kwargs):
        self.run(*args)




if __name__ == "__main__":


    @Teststep("Hallo Welt!!!")
    def doSomething(somearg, _teststep_, lala = "1", hoho = 2):
        print(_teststep_.id,':', _teststep_.desc)



    doSomething(1)
    print(doSomething.getInfo())
    print("doSomething is instance of Teststep:",
                                            isinstance(doSomething, Teststep))
