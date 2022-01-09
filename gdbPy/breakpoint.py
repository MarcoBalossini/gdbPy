import gdb

def info_breakpoints():
    """
    Get breakpoints info
    """
    # TODO: 
    return gdb.breakpoints()

def set_breakpoint(address):
    """
    Set a breakpoint in the code given the address.
    The address can be in various forms:
        - int number
        - string like '*0xB00B5'
        - string like '*main+n' ('*' is needed by gdb, it will be added if forgotten)
        - string like 'main'
    """
    # TODO: better with regex
    if isinstance(address, int):
        return gdb.Breakpoint(f"b *{hex(address)}")
    if isinstance(address, str):
        if address[0] == '*':
            return gdb.Breakpoint(f"b {address}")
        elif '+' in address:
            return gdb.Breakpoint(f"b *{address}")
        else:
            return gdb.Breakpoint(f"b {address}")
    
    print("[!] The argument must be an int or a string")
    return