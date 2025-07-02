import reader, printer
from mal_types import MalObj

import sys

def READ(raw_str: str) -> MalObj:
    return reader.read_str(raw_str)

def EVAL(malobj: MalObj) -> MalObj:
    return malobj

def PRINT(malobj: MalObj) -> str:
    return printer.pr_str(malobj,print_readably=True)

def repl(raw_str: str) -> str:
    proc_line=READ(raw_str)
    result=EVAL(proc_line)
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
            print(repl(raw_str))
