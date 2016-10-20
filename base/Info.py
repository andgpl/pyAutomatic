#! /usr/bin/python3
from Base import Base


class Info:


    def __init__(self, obj, children = []):
    
        if not isinstance(obj, Base.Base):
            # Should not happen
            # TODO: Raise exception
            return
    
        self.name        = obj.name
        self.id          = obj.id
        self.description = obj.desc
        self.children    = children
