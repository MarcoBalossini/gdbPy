import gdb

def start(stdin=None, stdout=None, stderr=None, params=[]):
    """
    Start the execution of a process and stop at the start

    :param str stdin: Optional stdin redirection. Default: none
    :param str stdout: Optional stdout redirection. Default: none
    :param str stderr: Optional stderr redirection. Default: none
    :param list[str] params: An optional list of parameters. Default: empty list
    """
    cmd = __concatenate_params("start", stdin, stdout, stderr, params)

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def run(stdin=None, stdout=None, stderr=None, params=[]):
    """
    Start the execution of a process

    :param str stdin: Optional stdin redirection. Default: none
    :param str stdout: Optional stdout redirection. Default: none
    :param str stderr: Optional stderr redirection. Default: none
    :param list[str] params: An optional list of parameters. Default: empty list
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
    try:
        gdb.execute("continue")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def next_instruction(c_level=False, repeat=1):
    """
    Go to next instruction (source line) but don't dive into functions

    :param bool c_level: Whether or not we consider the C instructions instead of the assembly ones
    :param int repeat: How many times to execute the command
    """

    if c_level:
        cmd = f"next {repeat}"
    else:
        cmd = f"nexti {repeat}"
    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def step_in(c_level=False):
    """
    Step to the next instruction diving into functions

    :param bool c_level: Whether or not we consider the C instructions instead of the assembly ones
    """

    if c_level:
        cmd = "step"
    else:
        cmd = "stepi"
    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def finish_function():
    """
    Continue until the current function returns.
    """
    
    try:
        gdb.execute("fin")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def kill_execution():
    """
    Kill current execution
    """
    try:
        gdb.execute("kill")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def set_argument(name, value, variable=True):
    """
    Set a runtime value
    :param name: The value to set
    :param value: The new value
    :param bool variable: If the value is a variable. Default is `True`
    """
    try:
        gdb.execute(f"set {'variable ' if variable==True else ''}{name} = {value}")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def return_to_caller(expression=""):
    """
    Return the expression to the caller
    :param str expression: The expression to return. Default is an empty string.
    """
    try:
        gdb.execute("return "+expression)
    except Exception as e:
        print(f"[!] ERROR: {e}")

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