#! /usr/bin/python3
import inspect



class DecoratorMeta(type):

    def __instancecheck__(cls, other):
        return isinstance(other, cls.__DecoBaseClass__)


    def __subclasscheck__(cls, other):
        return issubclass(other, cls.__DecoBaseClass__)





class Decorator(metaclass = DecoratorMeta):

    """ 
    This class is a decorator factory and also serves as the base class for
    the decorators used in this project. IT SHOULD NEVER BE INSTANTIATED
    DIRECTLY. Only via the static factory method "createDecorator". The
    generated decorator implements a special inheritance and instantiation
    procedure:
        
            @Decorator.createDecorator
            class Base:
                def __init__(self, _id, a, b):
                    ...
            
            
            @Base(argA, argB)
            class Sub:
                ...
                

    Is the same as:


            class Base:
                def __init__(self, _id, a, b):
                    ...           
                    
            class Sub(Base):
                def __init__(self, a, b)
                    super(Base, self).__init__(generateID(), a, b)
                    ...
            
                     
    It allows the currying of base class constructor arguments and generates
    an ID for Sub instances automatically. When wrapping a function with a
    generated decorator...
    
            @Base(argA, argB)
            def Func(self):
                ...                
    
    ... Base will be subclassed with Func as a member function with the same
    name. The decorator will return the instance of that new subclass.
    Accessing Func will then look like this:
    
            Func.Func()
    """


    def __new__(cls, *args, **kwargs):

        obj = super(Decorator, cls).__new__(cls)
        
        if (len(args) > 0) and\
                      (inspect.isclass(args[0]) or inspect.isfunction(args[0])):

            # First argument is a function or class
            # this is the object that is going to be
            # wrapped by this Decorator instance.
            # This also means the deocrator has not
            # received any arguments.
            cls.__init__(obj, *args, **kwargs)

            if obj._initDone:
                return cls._inheritFromBaseClass(obj)
            else:
                # This should not happen
                # TODO: raise exception
                pass
            
        else:
            # Decorator has received arguments that
            # do not contain the wrapped object.
            return obj



    def __init__(self, *args, **kwargs):

        self._initDone = False


        # Wrapped class or function
        self._wrappedObject = None


        # Base class for the wrapped object
        self._baseClass = self.__class__.__DecoBaseClass__
        self._baseClassArgs   = []
        self._baseClassKWargs = {}
        self._id = Decorator.getID()


        # Call actual initializer function
        self._initializer(args, kwargs)




    def __call__(self, *args, **kwargs):
            
        self._initializer(args, kwargs)
            
        if self._initDone:
            return self._inheritFromBaseClass()
        else:
            # TODO: something went wrong with the initialisation
            # raise exception
            pass





    def _initializer(self, args, kwargs):

        if self._initDone:
            return


        if (len(args) > 0) and\
                    (inspect.isclass(args[0]) or inspect.isfunction(args[0])):

            # First argument is a class or function
            self._wrappedObject = args[0]
            self._initDone = True

        else:
            # There is no argument given or first
            # argument is not a function or class      
            self._baseClassArgs   = args
            self._baseClassKWargs = kwargs





    def _inheritFromBaseClass(self):
        
    
    
        id_     = self._id
        args    = self._baseClassArgs
        kwArgs  = self._baseClassKWargs

        base = self._baseClass
        def init(self):
            super(self.__class__, self).__init__(id_, *args, **kwArgs)
                                    
        
        name    = self._wrappedObject.__name__
        bases   = (self._baseClass,)
        clsDict = {"__init__" : init}
                
        
        if inspect.isclass(self._wrappedObject):
            bases = (self._wrappedObject,) + bases
            
            
        elif inspect.isfunction(self._wrappedObject):
            clsDict[name] = staticmethod(self._wrappedObject)
            
            
        else:
            # This should not happen: wrapped object is neither a class nor
            # a function. TODO: raise exception
            pass
            


        cls = type(name, bases, clsDict)
        if inspect.isfunction(self._wrappedObject):
            return cls()
        else:
            return cls        



    @staticmethod
    def createDecorator(_class):
          
        if not inspect.isclass(_class):
            # TODO: raise exception
            return


        return type(_class.__name__, (Decorator,), {'__DecoBaseClass__':_class})
        


    __ID__ = 1
    @staticmethod
    def getID():
        Decorator.__ID__ += 1
        return Decorator.__ID__









if __name__ == "__main__":

    
    class NotMyBase:
        pass


    class MyBase:
        pass



    @Decorator.createDecorator
    class TestSuite(MyBase):

        def __init__(self, id_, desc = "", timeout = -1.0):

            self.id      = id_
            self.name    = self.__class__.__name__
            self.desc    = desc
            self.timeout = timeout

        def run(self):
            print(self.id, self.name, repr(self.desc), self.timeout)



    @TestSuite("lalal", 5.0)
    class Tests:

        def myFunction(self):
            print("my id is:", self.id)


 
    
    myTest = Tests()
    myTest.myFunction()
    myTest.run()
    print("myTest is an instance of MyBase:",    isinstance(myTest, MyBase))
    print("myTest is an instance of NotMyBase:", isinstance(myTest, NotMyBase))
    print("myTest is an instance of TestSuite:", isinstance(myTest, TestSuite))
    print("myTest is an instance of Tests:",     isinstance(myTest, Tests))
    
    print("Tests is subclass of MyBase:",     issubclass(Tests, MyBase))
    print("Tests is subclass of NotMyBase:",  issubclass(Tests, NotMyBase))
    print("Tests is subclass of Testsuite:",  issubclass(Tests, TestSuite))


    #------ Wrapping a function -------

    @TestSuite("Hallo Welt")
    def testFunc():
        print("inside testFunc.")
        
        
    testFunc.testFunc()
    testFunc.run()



