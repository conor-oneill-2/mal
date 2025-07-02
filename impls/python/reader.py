import re
from typing import List

from mal_types import *

class Reader:
    __slots__=["tokens","pos"]
    def __init__(self,tokens: List[str]):
        self.tokens=tokens
        self.pos=0
    
    def next(self) -> str:
        pos=self.pos
        self.pos+=1
        return self.tokens[pos]
    
    def peek(self) -> str:
        return self.tokens[self.pos]

def read_str(raw_str: str) -> MalObj:
    tokens=tokenize(raw_str)
    reader=Reader(tokens)
    return read_form(reader)

def tokenize(raw_str: str) -> List[str]:
    regex_str=r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""
    return re.findall(regex_str,raw_str)

def read_form(reader: Reader) -> MalObj:
    tok=reader.next()
    if tok in "([{":
        return read_list(reader,tok)
    elif tok in ["'","`","~","~@","@","^"]:
        return read_argument(reader,tok)
    else:
        return read_atom(tok)

def read_argument(reader: Reader,tok:str) -> MalList:
    if tok=="^":
        first_tok=read_form(reader)
        second_tok=read_form(reader)
        return MalList([
            MalSym('with-meta'),
            second_tok,
            first_tok
        ])
    
    if tok=="'":
        malobj=MalSym('quote')
    elif tok=="`":
        malobj=MalSym('quasiquote')
    elif tok=="~":
        malobj=MalSym('unquote')
    elif tok=="~@":
        malobj=MalSym('splice-unquote')
    elif tok=="@":
        malobj=MalSym('deref')
    return MalList([malobj,read_form(reader)])

def read_list(reader: Reader,start_tok:str) -> MalList:
    close_match={"(":")","[":"]","{":"}"}
    tok=reader.peek()
    malobjs=[]
    while tok!=close_match[start_tok]:
        malobjs.append(read_form(reader))
        tok=reader.peek()
    #If token is closing bracket, advance position to next token
    tok=reader.next()
    return MalList(malobjs,start_tok,close_match[start_tok])

def read_atom(tok: str) -> MalObj:
    if tok=="nil":
        return MalNil()
    if tok=="true":
        return MalBool(True)
    if tok=="false":
        return MalBool(False)
    if tok[0]==":":
        return MalKeyWord(tok[1:])
    #If token starts and ends with double quotes
    if tok[0]=='"' and tok[-1]=='"':
        return read_mal_str(tok[1:-1])
    try:
        val=int(tok)
        return MalInt(val)
    except ValueError:
        return MalSym(tok)

def read_mal_str(tok: str) -> MalStr:
    pos=0
    mal_str=""
    while pos < len(tok):
        char=tok[pos]
        pos+=1
        if char=="\\":
            char=tok[pos]
            if char in ["\\","\""]:
                mal_str+=char
                pos+=1
            if char=="n":
                mal_str+="\n"
                pos+=1
            continue
        mal_str+=char
    return MalStr(mal_str)