def READ(*args):
    return args[0]

def EVAL(*args):
    return args[0]

def PRINT(*args):
    return args[0]

def rep(raw_str):
    proc_line=READ(raw_str)
    result=EVAL(proc_line)
    output=PRINT(result)
    return output

if __name__=="__main__":
    while True:
        raw_str=input("user> ")
        print(rep(raw_str))
