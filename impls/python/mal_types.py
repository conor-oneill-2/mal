from typing import List

class MalObj:
    pass

class MalList(MalObj):
    __slots__=["objs","start_tok","end_tok"]
    def __init__(self,objs: List[MalObj],start_tok="(",end_tok=")"):
        self.objs=objs
        self.start_tok=start_tok
        self.end_tok=end_tok
    
    def __str__(self):
        result=" ".join(map(lambda x: str(x),self.objs))
        return self.start_tok+result+self.end_tok

class MalInt(MalObj):
    __slots__="val"
    def __init__(self,val:int):
        self.val=val
    
    def __str__(self):
        return str(self.val)

class MalSym(MalObj):
    __slots__="sym"
    def __init__(self,sym:str):
        self.sym=sym
    
    def __str__(self):
        return self.sym

class MalNil(MalObj):
    def __str__(self):
        return "nil"

class MalBool(MalObj):
    __slots__="bool"
    def __init__(self,bool:bool):
        self.bool=bool
    
    def __str__(self):
        return str(self.bool).lower()

class MalStr(MalObj):
    __slots__="val"
    def __init__(self,val:str):
        self.val=val
    
    def __str__(self):
        return '"'+self.val+'"'
    
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

class MalKeyWord(MalObj):
    __slots__="keyword"
    def __init__(self,keyword):
        self.keyword=keyword
    
    def __str__(self):
        return ":"+self.keyword