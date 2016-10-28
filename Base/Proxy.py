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
    '__ror__'
]

_computeInplaceNames = [
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
    '__setitem__',
    '__delitem__',
    'append',
    'update',
    'extend',
    'insert',
    'remove',
    'pop',
    'clear',
    'sort',
    'reverse'
]
    
_containerNames = [
    '__len__',
    '__length_hint__',
    '__getitem__',
    '__missing__',
    '__contains__',
    '__iter__',
    'index',
    'count',
    'copy',
    'fromkeys',
    'has_key',
    'keys,',
    'values',
    'items',
    '__reversed__'
]

_stringNames = [
    'capitalize',
    'casefold',
    'center',
    'count',
    'encode',
    'endswith',
    'expandtabs',
    'find',
    'format',
    'format_map',
    'index',
    'isalnum',
    'isalpha',
    'isdecimal',
    'isdigit',
    'isidentifier',
    'islower',
    'isnumeric',
    'isprintable',
    'isspace',
    'istitle',
    'isupper',
    'join',
    'ljust',
    'lower',
    'lstrip',
    'maketrans',
    'partition',
    'replace',
    'rfind',
    'rindex',
    'rjust',
    'rpartition',
    'rsplit',
    'rstrip',
    'split',
    'splitlines',
    'startswith',
    'strip',
    'swapcase',
    'title',
    'translate',
    'upper',
    'zfill'
]

_reprNames = [
    '__repr__',
    '__str__'
]

_specialNames = list(set(_computeNames + _computeInplaceNames +
                         _compareNames + _convertNames +
                         _containerAccessNames + _containerNames +
                         _stringNames + _reprNames))
                         
_mutableNames = list(set(_containerAccessNames))







def createWrapperMethod(func, raiseOnModify = False):

    if raiseOnModify:
        def wrappedFunc(self, *args, **kwargs):
            raise AttributeError("Object is immutable")
    else:
        def wrappedFunc(self, *args, **kwargs):
            args = (self._obj,) + args
            return func(*args, **kwargs)
            
    return wrappedFunc
    
    





class ProxyMeta(type):
    _typeCache = {}

    def __new__(cls, name, bases, namespace, basetype=int, immutable = False):
    
        ibName = basetype.__name__ + ('.immutable' if immutable else '')
    
        if ibName not in ProxyMeta._typeCache:
        
            fnDict = {}
            for name, member in inspect.getmembers(basetype):
                if name in _specialNames:
                
                    if not immutable:
                        fnDict[name] = createWrapperMethod(member)
                        
                    elif name in _mutableNames:
                        fnDict[name] = createWrapperMethod(member, True)
                     
                    else:
                        fnDict[name] = createWrapperMethod(member)
                    
                    
            if len(fnDict):
                ProxyMeta._typeCache[ibName] = dict(fnDict)

        else:
            fnDict = dict(ProxyMeta._typeCache[ibName])
    
    
        fnDict.update(namespace)
        proxy = super().__new__(cls, name, bases, fnDict)
        proxy._basetype  = basetype
        return proxy
    
    
    def __init__(cls, name, bases, namespace, basetype=int, immutable = False):
        pass
    



                

class Proxy(metaclass = ProxyMeta):  

    def __init__(self, value = None):
    
        if value is None:
            self._obj = self.__class__._basetype()
        else:
            self._obj = self.__class__._basetype(value)


class MyProxy(Proxy, basetype = str):
    pass


if __name__ == "__main__":
    p  = Proxy(10)
    p += 10
    print(p, type(p))
    
