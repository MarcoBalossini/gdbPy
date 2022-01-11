import os
import psutil

def launch_gdb(filename):
    os.execl("/usr/bin/gdb", "/usr/bin/gdb", "-q", "-x", filename)
    #os.system(f"gdb -q -x {filename}")

process = psutil.Process(os.getpid())
process_name = process.name()

if "python" in process_name:
    for arg in process.cmdline():
        if ".py" in arg:
            launch_gdb(arg)