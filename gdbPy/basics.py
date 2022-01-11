import gdb

def set_file(filename):
    """
    Sets a file in gdb, given its name

    :param str filename: the name of the file to debug
    """
    try:
        gdb.execute(f"file ./{filename}")
    except:
        print(f"[!] ERROR: File not set. {filename} is not a present executable")

def set_args(args):
    """
    Sets the argument to the execution

    :param list(str) args: optional arguments to use at the execution
    """
    try:
        cmd = "set args"
        for arg in args:
            cmd += f" {arg}"
        gdb.execute(cmd)
    except:
        print("[!] ERROR: args not set")

def execute(cmd):
    """
    Executes a generic command

    :param str cmd: The command
    """
    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def quit():
    """
    Quits and closes gdb
    """
    gdb.execute("quit")