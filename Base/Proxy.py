#! /usr/bin/python3
"""
See: http://code.activestate.com/recipes/496741-object-proxying/
"""
import inspect


_computeNames = [
    '__add__',
    '__sub__',
    '__mul__',
    '__matmul__',
    '__truediv__',
    '__floordiv__',
    '__mod__',
    '__divmod__',
    '__pow__',
    '__lshift__',
    '__rshift__',
    '__and__',
    '__xor__',
    '__or__',
    '__radd__',
    '__rsub__',
    '__rmul__',
    '__rmatmul__',
    '__rtruediv__',
    '__rfloordiv__',
    '__rmod__',
    '__rdivmod__',
    '__rpow__',
    '__rlshift__',
    '__rrshift__',
    '__rand__',
    '__rxor__',
    '__ror__',
    '__iadd__',
    '__isub__',
    '__imul__',
    '__imatmul__',
    '__itruediv__',
    '__ifloordiv__',
    '__imod__',
    '__ipow__',
    '__ilshift__',
    '__irshift__',
    '__iand__',
    '__ixor__',
    '__ior__'
]


_compareNames = [
    '__lt__',
    '__le__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__'
]


_convertNames = [
    '__neg__',
    '__pos__',
    '__abs__',
    '__invert__',
    '__complex__',
    '__int__',
    '__float__',
    '__round__',
    '__index__',
]

_containerAccessNames = [
    '__len__',
    '__length_hint__',
    '__getitem__',
    '__missing__',
    '__setitem__',
    '__delitem__',
    '__iter__',
    '__reversed__',
    '__contains__'
]

_specialNames = _computeNames + _compareNames + _convertNames +\
                _containerAccessNames



class ProxyMeta(type):

    def __init__(cls, name, bases, namespace, basetype = int, objName = "hoho"):
        cls.basetype = basetype
        setattr(cls, objname, basetype())
        

class CustomProxy(metaclass = ProxyMeta):  
    pass



    

if __name__ == "__main__":
    
    print(dir(CustomProxy()))
    print(int())
