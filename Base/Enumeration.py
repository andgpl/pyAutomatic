#! /usr/bin/python3
import collections
import operator



"""
Constants
"""
ENUM_DEFAULT_TYPE = int

ENUM_BASE_TYPE  = "__EnumBaseType__"
ENUM_VALUES     = "__EnumValues__"

ENUM_INIT_STATE = "__InitInProgress__"

ENUM_ERROR_ASSIGN = "Enumeration does not allow assignment"
ENUM_ERROR_DELETE = "Enumeration does not allow deletion"
ENUM_ERROR_TYPE   = "Values of {} must be of type '{}' but '{}' was found"
ENUM_ERROR_VALUE  = "Value '{}' already exists in {}"



class EnumValue:

    def __init__(self, name, value, enumCls):
    
        # Allow attribute assignment during initialisation
        object.__setattr__(self, ENUM_INIT_STATE, True)
    
        self.name  = name
        self.value = value
    
        # private
        self._basetype = enumCls.__EnumBaseType__
        self._enumCls  = enumCls
        
        
        delattr(self, ENUM_INIT_STATE)


    def __str__(self):
        return "{}.{} : {}".format(self._enumCls.__name__,
                                                    self.name, self.value)

    def __eq__(self, o):
        return self._compare(operator.eq, o)

    def __lt__(self, o):
        return self._compare(operator.lt, o)

    def __le__(self, o):
        return self._compare(operator.le, o)

    def __gt__(self, o):
        return self._compare(operator.gt, o)

    def __ge__(self, o):
        return self._compare(operator.ge, o)


    def _compare(self, op, o):
    
        if isinstance(o, self._basetype) and op(self.value, o):
            return True
            
        elif isinstance(o, EnumValue) and (self._basetype == o._basetype) and\
             op(self.value, o.value):
             return True
             
        else:
            return False


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
        if (bases == ()) or (bases == (Enumeration,)):
            setattr(cls, ENUM_BASE_TYPE, basetype)

            if bases != ():
                setattr(cls, ENUM_VALUES, [])
            

        # Parse class members into EnumValues.
        # - Allow only values of type __EnumBaseType__
        # - Allow only unique names
        # - Allow only unique values
        for name, value in namespace.items():       
            if name.startswith('_'):
                continue


            # Value must be instance of basetype
            if not isinstance(value, cls.__EnumBaseType__):
                raise TypeError(ENUM_ERROR_TYPE.format(cls.__name__,
                                                  cls.__EnumBaseType__.__name__,
                                                  type(value).__name__))


            # Value must be unique
            if value in cls.__EnumValues__:
                raise ValueError(ENUM_ERROR_VALUE.format(str(value),
                                                                cls.__name__))

            # Replace orignal value with EnumValue instance
            cls.__EnumValues__.append(value)
            setattr(cls, name, EnumValue(name, value, cls))
            
            
        # Disallow class modification after initialisation
        delattr(cls, ENUM_INIT_STATE)


    # EnumValues are considered instances of their Enumeration
    def __instancecheck__(cls, other):
        return isinstance(other, EnumValue) and issubclass(other._enumCls, cls)


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
