#! /usr/bin/python3
import collections
import operator

from Base.Proxy import Proxy

"""
Constants
"""
ENUM_DEFAULT_TYPE = int

ENUM_BASE_TYPE  = "__EnumBaseType__"
ENUM_VALUE_CLS  = "__EnumValueClass__"
ENUM_VALUES     = "__EnumValues__"

ENUM_INIT_STATE = "__InitInProgress__"

ENUM_ERROR_ASSIGN = "Enumeration does not allow assignment"
ENUM_ERROR_DELETE = "Enumeration does not allow deletion"
ENUM_ERROR_TYPE   = "Values of {} must be of type '{}' but '{}' was found"
ENUM_ERROR_VALUE  = "Value '{}'({}) already exists in {} ({})"
ENUM_ERROR_BASE   = ("Enumeration can only inherit from other Enumeration "
                     "class or subclass. '{}' is not an Enumeration.")
ENUM_ERROR_BASE_TYPE = ("Enumeration base classes must have the same base type."
                        " Type '{}' conflicts with '{}'.")



def createEnumValueClass(basetype):

    class EnumValue(Proxy, basetype = basetype, immutable = True):

        def __init__(self, name, value, enumCls):
        
      
            # Allow attribute assignment during initialisation
            object.__setattr__(self, ENUM_INIT_STATE, True)


            super(EnumValue, self).__init__(value)  
            
            # Private
            self._enumCls  = enumCls      
            self._enumName = enumCls.__name__
            
            # Public
            self.name      = name
            self.value     = self._obj
            
           
            # Denie write access
            delattr(self, ENUM_INIT_STATE)


        # Representations
        def __str__(self):
            return "{}.{} : {}".format(self._enumName, self.name, self.value)


        # EnumValues are immutable
        def __setattr__(self, name, value):
            if hasattr(self, ENUM_INIT_STATE):
                object.__setattr__(self, name, value)
            else:
                raise NotImplementedError(ENUM_ERROR_ASSIGN)
        
        
        def __delattr__(self, name):
            if hasattr(self, ENUM_INIT_STATE):
                object.__delattr__(self, name)
            else:
                raise NotImplementedError(ENUM_ERROR_DELETE)

    # Done
    return EnumValue



class EnumValueIndex:

    def __init__(self, cls):
        self._clsName = cls.__name__
        self._values  = collections.OrderedDict()
        self._names   = {}


    def append(self, ev):
    
        # Enumeration values must be unique
        if ev.value in self._values:
            raise ValueError(ENUM_ERROR_VALUE.format(str(ev.value), ev,
                                                     self._clsName,
                                                     self._values[ev.value]))

        self._values[ev.value] = ev
        if ev.name in self._names:
            del self._values[self._names[ev.name]]
        self._names[ev.name] = ev.value
        
       
    def update(self, *indeces):
        for index in indeces:
            for ev in index.list():
                self.append(ev)
           
        
    def list(self):
        return list(self._values.values())

        
    def items(self):
        return self._values.items()






class EnumMeta(type):

    @classmethod
    def __prepare__(metacls, name, bases, basetype = ENUM_DEFAULT_TYPE):
        return collections.OrderedDict()
    

    def __new__(cls, name, bases, namespace, basetype = ENUM_DEFAULT_TYPE):
        return super().__new__(cls, name, bases, dict(namespace))


    def __init__(cls, name, bases, namespace, basetype = ENUM_DEFAULT_TYPE):

        # Allow class modification during initialisation
        type.__setattr__(cls, ENUM_INIT_STATE, True)


        # __EnumBaseType__ holds the underlying type of the enumeration
        # This value can be set via the basetype keyword argument during
        # enum creation:
        #
        #   class MyEnum(Enumeration, basetype = <type>):
        #       ...
        #
        # A basetype can only be defined during the instantiation of the
        # Enumeration class (the default basetype) or when a custom
        # Enumeration is created (see above). When inherting from an
        # Enumeration class the basetype type of the parent Enumeration is
        # used, A possible basetype argument is ignored.
        #
        # __EnumValues__ holds the actual values of the enum. It is used to
        # detect multiple occurences of the same value
        #
        # __EnumValueClass__ holds the type specific class for this enum
        #
        if (bases == ()) or (bases == (Enumeration,)):
            setattr(cls, ENUM_BASE_TYPE, basetype)
            setattr(cls, ENUM_VALUE_CLS, createEnumValueClass(basetype))

            if bases != ():
                # This is a new enumeration internal enum value list is empty...
                setattr(cls, ENUM_VALUES, EnumValueIndex(cls))


        else:
            # This is an enumeration that inherits from other classes...
            
            
            # Enumeration can only inherit from other enumerations
            for ib in filter(lambda b: not issubclass(b, Enumeration), bases):
                raise TypeError(ENUM_ERROR_BASE.format(ib.__name__))
            
            
            # Base enumeration classes must have the same base type
            baseTypes = map(lambda b: b.__EnumBaseType__, bases)
            mainBt = next(baseTypes)
            for bt in baseTypes:
                if bt != mainBt:
                    raise TypeError(ENUM_ERROR_BASE_TYPE.format(mainBt.__name__,
                                                                bt.__name__))
                
            
            
            # Create new enum value index from base indeces
            baseIndeces = list(map(lambda b: b.__EnumValues__, bases))
            newIndex = EnumValueIndex(cls)
            newIndex.update(*baseIndeces)
            setattr(cls, ENUM_VALUES, newIndex)
        



        # Parse class members into EnumValues.
        # - Allow only values of type __EnumBaseType__
        # - Allow only unique names
        # - Allow only unique values
        for name, value in namespace.items():
            if name.startswith('_'):
                continue

            # Values can also be copied from other enumeration values
            #if isinstance(value, EnumValue):
            #    value = value.value


            # Replace orignal value with EnumValue instance
            ev = cls.__EnumValueClass__(name, value, cls)
            cls.__EnumValues__.append(ev)
            setattr(cls, name, ev)
            




        # Disallow class modification after initialisation
        delattr(cls, ENUM_INIT_STATE)


    # EnumValues are considered instances of their Enumeration
    def __instancecheck__(cls, ev):
        return isinstance(ev, cls.__EnumValueClass__) and\
               ((ev._enumCls == cls) or issubclass(cls, ev._enumCls))


    # Enumerations cannot be instanciated
    def __call__(cls):
        return cls
        

    # Enumerations are immutable
    def __setattr__(cls, name, value):

        if hasattr(cls, ENUM_INIT_STATE):
            type.__setattr__(cls, name, value)
        else:
            raise NotImplementedError(ENUM_ERROR_ASSIGN)
    
    
    def __delattr__(cls, name):

        if hasattr(cls, ENUM_INIT_STATE):
            type.__delattr__(cls, name)
        else:
            raise NotImplementedError(ENUM_ERROR_DELETE)
       


    # String functions
    def __str__(cls):
        
        r = cls.__name__ + '\n' + ('-' * len(cls.__name__))

        for ev in cls.__EnumValues__.list():
            r += '\n' + str(ev)

        return r



class Enumeration(metaclass = EnumMeta):
    pass





if __name__ == "__main__":

    class MyEnum(Enumeration, basetype = str):
        VAR = "Hallo"
        FOO = "1"
        BAR = "2"
        EGG = "3"


    class MyExtendedEnum(MyEnum):
        SPAM = "0"

    print(MyExtendedEnum.__EnumValues__)


    print(MyEnum.VAR, isinstance(MyEnum.VAR, MyEnum))
    print(MyExtendedEnum.VAR, isinstance(MyExtendedEnum.VAR, MyEnum))

    print("Hallo" == MyEnum.VAR)
    print(MyEnum.VAR < MyEnum.BAR)
    print(MyEnum.EGG == MyEnum.FOO)
    print(MyEnum.EGG >= MyEnum.FOO)
    print(MyEnum.EGG >= MyEnum.BAR)
    print(MyEnum())

    print(MyExtendedEnum.SPAM == MyEnum.BAR)
