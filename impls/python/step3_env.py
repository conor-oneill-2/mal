import reader, printer
from env import Env
from mal_types import *

import sys
from typing import Union

def make_base_env() -> Env:
    env=Env()
    env["+"]=lambda x,y: x+y
    env["-"]=lambda x,y: x-y
    env["*"]=lambda x,y: x*y
    env["/"]=lambda x,y: x//y
    return env

def READ(raw_str: str) -> MalObj:
    balanced=check_if_balanced(raw_str)
    if not balanced:
        raise MalError("Input is unbalanced.")
    return reader.read_str(raw_str)

def EVAL(malobj: MalObj,env:Env) -> MalObj:
    if "DEBUG-EVAL" in env:
        if env["DEBUG-EVAL"] not in [MalNil(),MalBool(False)]:
            debug_info=printer.pr_str(malobj,print_readably=True)
            print("EVAL: "+debug_info,file=sys.stderr)
    if type(malobj)==MalSym:
        #def! and let* require special handling
        #They get passed through and handled with their passed arguments
        if malobj.sym not in ["def!","let*"]:
            return env[malobj.sym]
    elif type(malobj)==MalList:
        if len(malobj.objs)>=1:
            #The first element in a list is the function to be applied
            func=EVAL(malobj.objs[0],env)
            return apply(func,malobj.objs[1:],env=env)


    elif type(malobj)==MalVector:
        return MalVector(list(map(lambda m: EVAL(m,env),malobj.objs)))
    elif type(malobj)==MalHashMap:
        return MalHashMap(list(map(lambda m: EVAL(m,env),malobj.objs)))
    return malobj

def apply(func:MalList,args:List[MalObj],env) -> MalObj:
    #def! special atom handling
    if func==MalSym("def!"):
        if len(args)!=2:
            raise MalError("Incorrect number of arguments in def! function")
        if type(args[0])!=MalSym:
            raise MalError(f"{args[0]} is not a valid variable name.")
        val=EVAL(args[1],env)
        env[args[0].sym]=val
        return val
    
    #let* special atom handling
    if func==MalSym("let*"):
        if len(args)!=2:
            raise MalError("Incorrect number of arguments in let* function")
        if type(args[0]) not in [MalList,MalVector]:
            raise MalError("First argument to let* function must be a list or vector")
        return eval_let(args[0],args[1],env)
        
    #default case
    eval_objs=list(map(lambda m: EVAL(m,env),args))
    return func(*eval_objs)

def eval_let(bindings:Union[MalList,MalVector],expr:MalObj,env:Env) -> MalObj:
    inner_env=Env(env)
    if len(bindings.objs)%2==1:
        raise MalError("Binding argument must come in pairs")
    i=0
    while i<len(bindings.objs):
        if type(bindings.objs[i])!=MalSym:
            raise MalError(f"{bindings.objs[i]} is not a valid symbol.")
        key=bindings.objs[i].sym
        kval=EVAL(bindings.objs[i+1],inner_env)
        inner_env[key]=kval
        i+=2
    return EVAL(expr,inner_env)
    
def PRINT(malobj: MalObj) -> str:
    return printer.pr_str(malobj,print_readably=True)

def rep(raw_str: str,env:Env) -> str:
    ast=READ(raw_str)
    result=EVAL(ast, env)
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
                #print("Input is unbalanced",file=sys.stderr)
                return False
            elif c==close_match[st[-1]]:
                st.pop()
            else:
                #print("Input is unbalanced",file=sys.stderr)
                return False


    if st!=[] or in_string:
        #print("Input is unbalanced",file=sys.stderr)
        return False
    else:
        return True


if __name__=="__main__":
    env=make_base_env()
    while True:
        raw_str=input("user> ")
        try:
            print(rep(raw_str,env))
        except MalError as e:
            print(e,file=sys.stderr)