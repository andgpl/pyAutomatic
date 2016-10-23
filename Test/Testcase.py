#! /usr/bin/python3

from Base.Base       import Base
from Base.Decorator  import Decorator
from Test.Teststep   import Teststep




@Decorator.createDecorator
class Testcase(Base):


    def __init__(self, _id, desc=""):
        super(Testcase.__DecoBaseClass__, self).__init__(_id, desc)
        
        
        # We only want teststeps as children:
        self._children = list(filter(lambda c: isinstance(c, Teststep),
                                                                self._children))
  

    def run(self):   
    
        self.setup()
    
        for child in self._children:
            child(self)

        self.teardown()
        


    def setup(self):
        pass

    
    def teardown(self):
        pass





if __name__ == "__main__":


    @Testcase
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


    m = MyCase()
    m.run()
    
