import gdb

def start(stdin=None, stdout=None, stderr=None, params=[]):
    """Start the execution of a process and stop at the start

    Args:
        stdin (str, optional): stdin redirection. Defaults to None.
        stdout (str, optional): stdout redirection. Defaults to None.
        stderr (str, optional): stderr redirection. Defaults to None.
        params (list, optional): An optional list of parameters. Defaults to [].
    """
    cmd = __concatenate_params("start", stdin, stdout, stderr, params)

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def run(stdin=None, stdout=None, stderr=None, params=[]):
    """Start the execution of a process

    Args:
        stdin (str, optional): stdin redirection. Defaults to None.
        stdout (str, optional): stdout redirection. Defaults to None.
        stderr (str, optional): stderr redirection. Defaults to None.
        params (list, optional): An optional list of parameters. Defaults to [].
    """
    cmd = __concatenate_params("run", stdin, stdout, stderr, params)

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def continue_exec():
    """Continues execution
    """
    try:
        gdb.execute("continue")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def next_instruction(c_level=False, repeat=1):
    """Go to next instruction (source line) but doesn't dive into functions

    Args:
        c_level (bool, optional): Whether or not we consider the C instructions instead of the assembly ones. Defaults to False.
        repeat (int, optional): How many times to execute the command. Defaults to 1.
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
    """Step to the next instruction diving into functions

    Args:
        c_level (bool, optional): Whether or not we consider the C instructions instead of the assembly ones. Defaults to False.
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
    """Continue until the current function returns.
    """
    
    try:
        gdb.execute("fin")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def kill_execution():
    """Kills current execution
    """
    try:
        gdb.execute("kill")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def set_argument(name, value, variable=True):
    """Set a runtime value

    Args:
        name (str): The value to set
        value (str): The new value
        variable (bool, optional): [description]. Defaults to True.
    """
    try:
        gdb.execute(f"set {'variable ' if variable==True else ''}{name} = {value}")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def return_to_caller(expression=""):
    """Return the expression to the caller

    Args:
        expression (str, optional): The expression to return. Defaults to "".
    """
    try:
        gdb.execute("return "+expression)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def __concatenate_params(cmd, stdin, stdout, stderr, params):
    """Concatenate params to a given command

    Args:
        cmd (str): The command with no parameters
        stdin (str): stdin redirection
        stdout (str): stdout redirection
        stderr (str): stderr redirection
        params (list[str]): An optional list of parameters

    Returns:
        str: The command filled with parameters
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