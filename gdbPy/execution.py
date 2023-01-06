import gdb

class Thread:
    def __init__(self, thread: gdb.Thread):
        self.__thread = thread
    
    def get_name(self) -> str:
        """Returns the thread's name"""
        return self.__thread.name
    def set_name(self, name: str) -> None:
        """Sets the thread's name"""
        self.__thread.name = name

    def get_num(self) -> int:
        """Returns the thread's number"""
        return self.__thread.num
    
    def get_global_num(self) -> int:
        """Returns the thread's global number"""
        return self.__thread.global_num

    def get_ptid(self) -> tuple[int, int, int]:
        """Returns the thread's ptid"""
        return self.__thread.ptid

    def get_inferior(self) -> Inferior:
        """Returns the thread's inferior"""
        return Inferior(self.__thread.inferior)

    def get_details(self) -> str|None:
        """Returns the thread's details"""
        return self.__thread.details

    def is_valid(self) -> bool:
        """Returns whether the thread is valid or not"""
        return self.__thread.is_valid()

    def is_exited(self) -> bool:
        """Returns whether the thread is exited or not"""
        return self.__thread.is_exited()

    def is_stopped(self) -> bool:
        """Returns whether the thread is stopped or not"""
        return self.__thread.is_stopped()

    def is_running(self) -> bool:
        """Returns whether the thread is running or not"""
        return self.__thread.is_running()

    def switch_thread(self) -> None:
        """Changes GDB’s currently selected thread to the one represented by this object"""
        self.__thread.switch()

    def handle(self) -> bytes:
        """Returns a gdb.Handle object for the thread"""
        return self.__thread.handle()
    
class Inferior:
    def __init__(self, inferior: gdb.Inferior):
        self.__inferior = inferior

    def get_num(self) -> int:
        """Returns the inferior's number"""
        return self.__inferior.num
    
    def get_connection(self) -> gdb.TargetConnection:
        """Returns the inferior's connection"""
        return self.__inferior.connection

    def get_connection_num(self) -> int:
        """Returns the inferior's connection number"""
        return self.__inferior.connection_num

    def get_pid(self) -> int:
        """Returns the inferior's pid"""
        return self.__inferior.pid

    def was_attached(self) -> bool:
        """Returns whether the inferior was attached or not"""
        return self.__inferior.was_attached()

    # TODO: Add progspaces?
    # def get_progspace(self) -> gdb.ProgSpace:
    #     """Returns the inferior's program space"""
    #     return self.__inferior.progspace

    def is_valid(self) -> bool:
        """Returns whether the inferior is valid or not"""
        return self.__inferior.is_valid()

    def threads(self) -> list[Thread]:
        """Returns a list of all threads in the inferior"""
        return [Thread(t) for t in self.__inferior.threads()]

    # TODO: Add architectures?
    # def get_architecture(self) -> gdb.Architecture:
    #     """Returns the inferior's architecture"""
    #     return self.__inferior.architecture

    # TODO: Understand memoryview objects
    # def read_memory(self, address: int, length: int) -> bytes:
    #     """Reads the inferior's memory

    #     Args:
    #         address (int): The address to read from
    #         length (int): The length to read

    #     Returns:
    #         bytes: The read data
    #     """
    #     return self.__inferior.read_memory(address, length)

    def write_memory(self, address: int, data: bytes) -> None:
        """Writes to the inferior's memory

        Args:
            address (int): The address to write to
            data (bytes): The data to write
        """
        self.__inferior.write_memory(address, data)

    def search_memory(self, address: int, len: int, data: bytes) -> int|None:
        """Searches for a pattern in the inferior's memory

        Args:
            address (int): The address to start searching from
            len (int): The length to search
            data (bytes): The data to search for

        Returns:
            int|None: The address of the pattern if found, None otherwise
        """
        return self.__inferior.search_memory(address, len, data)

    def thread_from_handle(self) -> Thread:
        """Returns the thread associated with the inferior's handle"""
        return Thread(self.__inferior.thread_from_handle())

def start(stdin: str|None =None, stdout: str|None =None, stderr: str|None =None, params: list[str] =[]) -> None:
    """Start the execution of a process and stop at the start

    Args:
        stdin (str, optional): stdin redirection. Defaults to None.
        stdout (str, optional): stdout redirection. Defaults to None.
        stderr (str, optional): stderr redirection. Defaults to None.
        params (list[str], optional): An optional list of parameters. Defaults to [].
    """
    cmd = __concatenate_params("start", stdin, stdout, stderr, params)

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def run(stdin: str|None =None, stdout: str|None =None, stderr: str|None =None, params: list[str] =[]) -> None:
    """Start the execution of a process

    Args:
        stdin (str, optional): stdin redirection. Defaults to None.
        stdout (str, optional): stdout redirection. Defaults to None.
        stderr (str, optional): stderr redirection. Defaults to None.
        params (list[str], optional): An optional list of parameters. Defaults to [].
    """
    cmd = __concatenate_params("run", stdin, stdout, stderr, params)

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def continue_exec() -> None:
    """Continues execution
    """
    try:
        gdb.execute("continue")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def next_instruction(c_level: bool =False, repeat : int =1) -> None:
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

def step_in(c_level: bool =False) -> None:
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

def finish_function() -> None:
    """Continue until the current function returns.
    """
    
    try:
        gdb.execute("fin")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def kill_execution() -> None:
    """Kills current execution
    """
    try:
        gdb.execute("kill")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def inferior() -> Inferior:
    """Returns the current inferior

    Returns:
        Inferior: The current inferior
    """
    return Inferior(gdb.selected_inferior())

def set_argument(name: str, value: str, variable: bool|None =True) -> None:
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

def return_to_caller(expression: str ="") -> None:
    """Return the expression to the caller

    Args:
        expression (str, optional): The expression to return. Defaults to "".
    """
    try:
        gdb.execute("return "+expression)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def __concatenate_params(cmd: str|None, stdin: str|None, stdout: str|None, stderr: str|None, params: list[str]) -> str:
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