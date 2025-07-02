import reader, printer
from mal_types import *

import sys

repl_env={
    "+": lambda x,y: x+y,
    "-": lambda x,y: x-y,
    "*": lambda x,y: x*y,
    "/": lambda x,y: x//y
}

def READ(raw_str: str) -> MalObj:
    return reader.read_str(raw_str)

def EVAL(malobj: MalObj,repl_env:dict) -> MalObj:
    if "DEBUG-EVAL" in repl_env:
        if repl_env["DEBUG-EVAL"] not in [MalNil(),MalBool(False)]:
            printer.pr_str(malobj)
    if type(malobj)==MalSym:
        if malobj.sym in repl_env:
            return repl_env[malobj.sym]
        else:
            print(f"Argument {malobj.sym} not found.",sys.stderr)
            return MalError()
    elif type(malobj)==MalList:
        if len(malobj.objs)>=1:
            eval_objs=list(map(lambda m: EVAL(m,repl_env),malobj.objs))
            return eval_objs[0](*eval_objs[1:])
    elif type(malobj)==MalVector:
        return MalVector(list(map(lambda m: EVAL(m,repl_env),malobj.objs)))
    elif type(malobj)==MalHashMap:
        return MalHashMap(list(map(lambda m: EVAL(m,repl_env),malobj.objs)))
    return malobj

def PRINT(malobj: MalObj) -> str:
    return printer.pr_str(malobj,print_readably=True)

def rep(raw_str: str) -> str:
    ast=READ(raw_str)
    result=EVAL(ast, repl_env)
    output=PRINT(result)
    return output

def check_if_balanced(raw_str):
    st=[]
    close_match={
        '(':')',
        '[':']',
        '{':'}'
    }
    ignore_next_char=False
    in_string=False
    for c in raw_str:
        if ignore_next_char:
            ignore_next_char=False
            continue
        
        if c=="\\":
            ignore_next_char=True
        elif c=='"':
            in_string=not in_string
        
        if in_string:
            continue

        if c==";":
            break
        
        elif c in "({[":
            st.append(c)
        elif c in ")}]":
            if st==[]:
                print("Input is unbalanced",file=sys.stderr)
                return False
            elif c==close_match[st[-1]]:
                st.pop()
            else:
                print("Input is unbalanced",file=sys.stderr)
                return False


    if st!=[] or in_string:
        print("Input is unbalanced",file=sys.stderr)
        return False
    else:
        return True

        


if __name__=="__main__":
    while True:
        raw_str=input("user> ")
        balanced=check_if_balanced(raw_str)
        if balanced:
            print(rep(raw_str))