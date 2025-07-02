from mal_types import *

def pr_str(malobj: MalObj,print_readably:bool):
    if type(malobj)==MalStr and print_readably:
        return malobj.print_readably()
    return str(malobj)