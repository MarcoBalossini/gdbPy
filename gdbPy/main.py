import gdb
import os

class SingletonMeta(type):
    """
    Meta class to implement singleton on `main_gdbPy`
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class main_gdbPy(metaclass=SingletonMeta):
    """
    Main library class, which contains all debug methods.
    The class comes as a singleton, since a special init is needed
    """

    def __init__(self):
        """
        Only at the first instruction called we start gdb.
        `-q` and `-x` options are useful to use gdb python module
        """
        # TODO: What to execute?
        os.system(f"gdb -q -x ...")

    def set_file(filename):
        """
        Sets a file in gdb, given its name
        """
        try:
            res = gdb.execute(f"file ./{filename}")
        except:
            print(f"[!] File not set. {filename} is not a present executable")

    def continue_exec():
        """
        Continue execution
        """
        gdb.execute("continue")

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

    def quit():
        """
        Quits and closes gdb
        """
        gdb.execute("quit")