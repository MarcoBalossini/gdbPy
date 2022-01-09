import gdb

def set_file(filename):
    """
    Sets a file in gdb, given its name

    :param str filename: the name of the file to debug
    """
    try:
        res = gdb.execute(f"file ./{filename}")
    except:
        print(f"[!] File not set. {filename} is not a present executable")

def start(stdin=None, stdout=None, stderr=None, params=[]):
    """
    Start the execution of a process and stop at the start

    :param str stdin: Optional stdin redirection
    :param str stdout: Optional stdout redirection
    :param str stderr: Optional stderr redirection
    :param list[str] params: An optional list of parameters
    """
    cmd = __concatenate_params("start", stdin, stdout, stderr, params)

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def run(stdin=None, stdout=None, stderr=None, params=[]):
    """
    Start the execution of a process

    :param str stdin: Optional stdin redirection
    :param str stdout: Optional stdout redirection
    :param str stderr: Optional stderr redirection
    :param list[str] params: An optional list of parameters
    """
    cmd = __concatenate_params("run", stdin, stdout, stderr, params)

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def continue_exec():
    """
    Continue execution
    """
    gdb.execute("continue")

def quit():
    """
    Quits and closes gdb
    """
    gdb.execute("quit")

def __concatenate_params(cmd, stdin, stdout, stderr, params):
    """
    Concatenate params to a given command

    :param str stdin: Optional stdin redirection
    :param str stdout: Optional stdout redirection
    :param str stderr: Optional stderr redirection
    :param list[str] params: An optional list of parameters
    """
    for p in params:
        cmd += f" {p}"
    
    if stdin != None:
        cmd += f" <{stdin}"
    if stdout != None:
        cmd += f" >{stdout}"
    if stderr != None:
        cmd += f" 2>{stderr}"
    return cmd