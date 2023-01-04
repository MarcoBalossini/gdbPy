import os
import psutil

def launch_gdb(filename: str):
    os.execl("/usr/bin/gdb", "/usr/bin/gdb", "-q", "-x", filename)

process = psutil.Process(os.getpid())
process_name = process.name()

if "gdb" not in process_name:
    for arg in process.cmdline():
        if ".py" in arg:
            launch_gdb(arg)
else:
    # set PWNLIB_NOTERM = 1 to avoid problems with pwntools
    os.environ["PWNLIB_NOTERM"] = "1"
    # import all files' methods
    from gdbPy.basics import *
    from gdbPy.info import *
    from gdbPy.execution import *
    from gdbPy.breakpoint import *
    from gdbPy.signals import *