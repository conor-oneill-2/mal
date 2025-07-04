from typing import List
import sys

class MalObj:
    def __call__(self):
        return self
    
    def __hash__(self):
        return hash(str(self))

class MalList(MalObj):
    __slots__="objs"
    def __init__(self,objs: List[MalObj]):
        self.objs=objs
    
    def __str__(self):
        result=" ".join(map(lambda x: str(x),self.objs))
        return "("+result+")"
    
    def __eq__(self,other):
        if type(other)!=MalList:
            return False
        if len(self.objs)!=len(other.objs):
            return False
        for selobj, othobj in zip(self.objs,other.objs):
            if selobj!=otherobj:
                return False
        return True

    def __hash__(self):
        return hash(str(self))

class MalVector(MalObj):
    __slots__="objs"
    def __init__(self,objs: List[MalObj]):
        self.objs=objs
    
    def __str__(self):
        result=" ".join(map(lambda x: str(x),self.objs))
        return "["+result+"]"

    def __eq__(self,other):
        if type(other)!=MalVector:
            return False
        if len(self.objs)!=len(other.objs):
            return False
        for selobj, othobj in zip(self.objs,other.objs):
            if selobj!=otherobj:
                return False
        return True

    def __hash__(self):
        return hash(str(self))

class MalHashMap(MalObj):
    __slots__="objs"
    def __init__(self,objs: List[MalObj]):
        self.objs=objs
    
    def __str__(self):
        result=" ".join(map(lambda x: str(x),self.objs))
        return "{"+result+"}"

    def __eq__(self,other):
        if type(other)!=MalHashMap:
            return False
        if len(self.objs)!=len(other.objs):
            return False
        for selobj, othobj in zip(self.objs,other.objs):
            if selobj!=otherobj:
                return False
        return True

    def __hash__(self):
        return hash(str(self))

class MalInt(MalObj):
    __slots__="val"
    def __init__(self,val:int):
        self.val=val
    
    def __add__(self,other):
        return MalInt(self.val+other.val)
    
    def __sub__(self,other):
        return MalInt(self.val-other.val)
    
    def __mul__(self,other):
        return MalInt(self.val*other.val)
    
    def __floordiv__(self,other):
        return MalInt(self.val//other.val)

    def __str__(self):
        return str(self.val)
    
    def __eq__(self,other):
        if type(other)!=MalInt:
            return False
        return self.val==other.val

    def __hash__(self):
        return hash(str(self))

class MalSym(MalObj):
    __slots__="sym"
    def __init__(self,sym:str):
        self.sym=sym
    
    def __str__(self):
        return self.sym
    
    def __eq__(self,other):
        if type(other)!=MalSym:
            return False
        return self.sym==other.sym

    def __hash__(self):
        return hash(str(self))

class MalNil(MalObj):
    def __str__(self):
        return "nil"
    
    def __eq__(self,other):
        return type(other)==MalNil

    def __hash__(self):
        return hash(str(self))

class MalBool(MalObj):
    __slots__="bool"
    def __init__(self,bool:bool):
        self.bool=bool
    
    def __str__(self):
        return str(self.bool).lower()
    
    def __eq__(self,other):
        if type(other)!=MalBool:
            return False
        return self.bool==other.bool

    def __hash__(self):
        return hash(str(self))

class MalStr(MalObj):
    __slots__="val"
    def __init__(self,val:str):
        self.val=val
    
    def __str__(self):
        return '"'+self.val+'"'
    
    def __eq__(self,other):
        if type(other)!=MalStr:
            return False
        return self.val==other.val

    def __hash__(self):
        return hash(str(self))
    
    def print_readably(self):
        f_str=self.val
        result=""
        for c in f_str:
            if c=="\n":
                result+=r"\n"
            elif c=="\\":
                result+=r"\\"
            elif c=='"':
                result+=r"\""
            else:
                result+=c
        return '"'+result+'"'

class MalWithMeta(MalObj):
    __slots__=["val","metadata"]
    def __init__(self,val,metadata):
        self.val=val
        self.metadata=metadata
    
    def __str__(self):
        return "with-meta "
    
    def __eq__(self,other):
        if type(other)!=MalWithMeta:
            return False
        return self.val==other.val and self.metadata == other.metadata

    def __hash__(self):
        return hash(str(self))

class MalKeyWord(MalObj):
    __slots__="keyword"
    def __init__(self,keyword):
        self.keyword=keyword
    
    def __str__(self):
        return ":"+self.keyword
    
    def __eq__(self,other):
        if type(other)!=MalKeyWord:
            return False
        return self.keyword==other.keyword

    def __hash__(self):
        return hash(str(self))