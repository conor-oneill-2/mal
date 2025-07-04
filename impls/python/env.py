from typing import Optional
import sys

from mal_types import MalObj, MalSym

class Env:
    __slots__=["outer","data"]
    def __init__(self,outer:Optional["Env"]=None):
        self.outer=outer
        self.data=dict()
    
    def __contains__(self,sym:MalSym)->bool:
        if sym in self.data:
            return True
        if self.outer!=None:
            return sym in self.outer
        return False
    
    def __getitem__(self,sym:MalSym) -> Optional[MalObj]:
        if sym in self.data:
            return self.data[sym]
        if self.outer!=None:
            return self.outer[sym]
        raise RuntimeError(f"'{sym}' not found.")
    
    def __setitem__(self,sym:MalSym,val=MalObj):
        self.data[sym]=val