#! /usr/bin/python3
import textwrap

from Base.Base import Base



class Info:


    def __init__(self, obj, children = []):
    
        if not isinstance(obj, Base):
            # Should not happen
            # TODO: Raise exception
            return
    
        self.name        = obj.name
        self.id          = obj.id
        self.description = obj.desc
        self.children    = children
        
        
        
    def __str__(self):
    
        r = '{}({}) : {}'.format(self.name, self.id, self.description)
        for child in self.children:
            r += '\n' + textwrap.indent(str(child), '    ')
            
        return r
