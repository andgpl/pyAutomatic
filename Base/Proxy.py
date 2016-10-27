#! /usr/bin/python3
"""
See: http://code.activestate.com/recipes/496741-object-proxying/
"""
import operator


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


class CustomProxy:

    _typeCache = {}
    
    
    def __new__(cls, obj):    
        return super(CustomProxy, cls).__new__(cls)
    

    def __init__(self, obj):
        self._obj = obj
        

        for name in dir(obj):
            setattr(self, name)

    

if __name__ == "__main__":
    
    pass
