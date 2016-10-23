#! /usr/bin/python3

from Base.Base       import Base
from Base.Decorator  import Decorator
from Test.Testcase   import Testcase



@Decorator.createDecorator
class Testsuite(Base):

    def __init__(self, _id, desc=""):
        super(Testsuite.__DecoBaseClass__, self).__init__(_id, desc)
        
        
        # We only want testcases as children:
        self._children = list(filter(lambda c: isinstance(c, Testcase),
                                                                self._children))


    def run(self):
        
        for child in self._children:
            child.run()
            
            

if __name__ == "__main__":

    from Teststep import Teststep


    @Testcase("My test step")
    class MyCase:
    
        def setup(self):
            self.stuffWeNeed = True
    
    
        @Teststep
        def firstDoThis(self):
            print("lala", self.stuffWeNeed)
            
            
        @Teststep
        def afterwardsThis(self, _teststep_):
            print("Hoho")
            print("Also my id is:", _teststep_.id)
            
            
        def teardown(self):
            print("Done")


    @Testsuite("My test suite")
    class MySuite:
    
        ts1 = MyCase()
        
        

    suite = MySuite()
    suite.run()
    print(suite.getInfo())
