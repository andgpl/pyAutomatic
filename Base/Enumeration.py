#! /usr/bin/python3
import inspect



class EnumValue:

    def __init__(self, enumCls, name, value):
        self._enumCls = enumCls
        self.name     = name
        self.value    = value

    def __str__(self):
        return "{}.{} : {}".format(self._enumCls.__name__,
                                                    self.name, self.value)

    def __eq__(self, o):
        return  (isinstance(o, int) and (self.value == o)) or\
                (isinstance(o, EnumValue) and\
                 issubclass(o._enumCls, self._enumCls) and\
                 self.value == o)

    def __lt__(self, o):
        return  (isinstance(o, int) and (self.value < o)) or\
                (isinstance(o, EnumValue) and\
                 issubclass(o._enumCls, self._enumCls) and\
                 self.value < o)

    def __le__(self, o):
        return  (isinstance(o, int) and (self.value <= o)) or\
                (isinstance(o, EnumValue) and\
                 issubclass(o._enumCls, self._enumCls) and\
                 self.value <= o)

    def __gt__(self, o):
        return  (isinstance(o, int) and (self.value > o)) or\
                (isinstance(o, EnumValue) and\
                 issubclass(o._enumCls, self._enumCls) and\
                 self.value > o)

    def __ge__(self, o):
        return  (isinstance(o, int) and (self.value >= o)) or\
                (isinstance(o, EnumValue) and\
                 issubclass(o._enumCls, self._enumCls) and\
                 self.value >= o)



class EnumMeta(type):

    def __init__(cls, name, bases, attrs):

        # Allow only values defined during class definition
        basevars = dir(type)
        for name, value in inspect.getmembers(cls):
            if not name.startswith('_') and name not in basevars:

                if not isinstance(value, int):
                    #TODO: Throw exception
                    continue

                print(name)
                setattr(cls, name, EnumValue(cls, name, value))


    def __instancecheck__(cls, other):
        return isinstance(other, EnumValue) and issubclass(other._enumCls, cls)


    def __call__(cls):
        # Enumeration cannot be instantiated
        return cls


class Enumeration(metaclass = EnumMeta):
    pass





if __name__ == "__main__":

    class MyEnum(Enumeration):
        VAR = 1
        FOO = 2
        BAR = 3
        EGG = 2


    class MyExtendedEnum(MyEnum):
        SPAM = 3

    print(MyEnum.VAR, isinstance(MyEnum.VAR, MyEnum))
    print(MyExtendedEnum.VAR, isinstance(MyExtendedEnum.VAR, MyEnum))

    print(MyEnum.VAR == 2)
    print(MyEnum.VAR < MyEnum.BAR)
    print(MyEnum.EGG == MyEnum.FOO)
    print(MyEnum.EGG >= MyEnum.FOO)
    print(MyEnum.EGG >= MyEnum.BAR)
    print(MyEnum())

    print(MyExtendedEnum.BAR == MyEnum.BAR)
