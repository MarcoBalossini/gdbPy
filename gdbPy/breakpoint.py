import gdb
from enum import Enum

# Commented types are present on the doc, but not effectively existing...
# These guys seems to know more than sourceware: https://www-zeuthen.desy.de/unix/unixguide/infohtml/gdb/Python-API.html#Python-API
class Break_type(Enum):
    """Types of breakpoint"""
    BREAKPOINT = 1
    #HARDWARE_BREAKPOINT = 
    WATCHPOINT = 6
    HARDWARE_WATCHPOINT = 7
    READ_WATCHPOINT = 8
    ACCESS_WATCHPOINT = 9
    #CATCHPOINT = 

# TODO: check indexes
class WP_Type(Enum):
    WP_READ = 1
    WP_WRITE = 0
    WP_ACCESS = 2

class Breakpoint():
    """
    A wrapper for class `gdb.Breakpoint`, sice there's few documentation of gdb python module
    Original object is still available for use (docs: https://sourceware.org/gdb/onlinedocs/gdb/Breakpoints-In-Python.html#Breakpoints-In-Python)

    Attributes:
        __breakpoint     The corresponding gdb.Breakpoint object
    """


    def __init__(self, breakpoint: gdb.Breakpoint):
        self.__breakpoint = breakpoint
  
    def get_number(self) -> int:
        """Returns breakpoint number"""
        return self.__breakpoint.number

    def get_type(self) -> str:
        """Returns breakpoint type as a string"""
        return Break_type(self.__breakpoint.type)

    def is_temporary(self) -> bool:
        """Returns whether the checkpoint is temporary or not"""
        return self.__breakpoint.temporary

    def is_valid(self) -> bool:
        """Returns whether the breakpoint is still valid or not"""
        return self.__breakpoint.is_valid()

    def delete(self) -> None:
        """Delete the breakpoint"""
        self.__breakpoint.delete()

    def is_enabled(self) -> bool:
        """Returns whether the breakpoint is enabled or not"""
        return self.__breakpoint.enabled

    def is_silent(self) -> bool:
        """Returns whether the breakpoint is silent or not"""
        return self.__breakpoint.silent

    def is_pending(self) -> bool:
        """Returns whether the breakpoint is pending or not"""
        return self.__breakpoint.pending

    def get_thread(self) -> int|None:
        """If breakpoint is thread specific returns the thread's global id, otherwise returns `None`"""
        return self.__breakpoint.thread

    def get_ignore_count(self) -> int:
        """Returns the ignore count"""
        return self.__breakpoint.ignore_count

    def is_visible(self) -> bool:
        """Returns whether the breakpoint is visible or not"""
        return self.__breakpoint.visible
    
    def get_count(self) -> int:
        """Returns breakpoint's hit count"""
        return self.__breakpoint.hit_count

    def get_location(self) -> str|None:
        """Returns breakpoint's location as a string. None if the breakpoint does not have one"""
        return self.__breakpoint.location

    def get_expression(self) -> str|None:
        """Returns breakpoint's expression as a string. None if the breakpoint does not have one"""
        return self.__breakpoint.expression

    def get_condition(self) -> str|None:
        """Returns breakpoint's condition as a string. None if the breakpoint does not have one"""
        return self.__breakpoint.condition

    def get_commands(self) -> str|None:
        """
        Returns breakpoint's commands as a string (commands are separated by a new line character).
        None if the breakpoint does not have one.
        """
        return self.__breakpoint.condition


    # setters
    def enable(self) -> None:
        """Enable the breakpoint"""
        self.__breakpoint.enabled = True

    def disable(self) -> None:
        """Disable the breakpoint"""
        self.__breakpoint.enabled = False

    def silence(self) -> None:
        """Silence the breakpoint"""
        self.__breakpoint.silent = True

    def unsilence(self) -> None:
        """Unsilence the breakpoint"""
        self.__breakpoint.silent = False

    def set_thread(self, thread_id: int) -> None:
        """
        Set the thread id to the breakpoint
        
        Args:
            thread_id (int): The thread id
        """
        self.__breakpoint.thread = thread_id

    def set_ignore_count(self, ignore: int) -> None:
        """
        Sets the ignore count
        Args:
            ignore (int): The ignore count
        """
        self.__breakpoint.ignore_count = ignore

    def reset_hit_count(self) -> None:
        """Resets hit count"""
        self.__breakpoint.hit_count = 0

    def set_condition(self, condition: str) -> None:
        """
        Sets the breakpoint's condition
        Args:
            condition (str): The condition string to be set
        """
        self.__breakpoint.condition = condition

    # TODO: Still some problem
    def set_commands(self, commands: str) -> None:
        """
        Sets the breakpoint's command
        Args:
            command (str): The command string to be set
        """
        self.__breakpoint.commands = commands


def get_breakpoints() -> list[Breakpoint]:
    """
    Get breakpoints info.
    """
    breakpoints = gdb.breakpoints()
    return [Breakpoint(b) for b in breakpoints]

def set_breakpoint(address: int|str, is_temporary=False) -> Breakpoint|None:
    """Set a breakpoint in the code given the address.

    Args:
        address (int, str): The int address or a valid string for command break
        is_temporary (bool, optional): Whether to create a temporary breakpoint or a permanent one. Defaults to False.

    Returns:
        (Breakpoint, None): The newly created breakpoint object None if couldn't create one
    """
    return __set_general_break(address, gdb.BP_BREAKPOINT, is_temporary)

def set_hardware_breakpoint(address: int, is_temporary=False) -> Breakpoint|None:
    """Set a hardware breakpoint in the code given the address.

    Args:
        address (int, str): The int address or a valid string for command break
        is_temporary (bool, optional): Whether to create a temporary breakpoint or a permanent one. Defaults to False.

    Returns:
        (Breakpoint, None): The newly created hardware breakpoint object. None if couldn't create one
    """
    # gdb.BP_HARDWARE_BREAKPOINT seems to not really exist on gdb module (their type is gdb.BP_BREAKPOINT)
    # We'll use a "rustic" way to obtain a  hardware breakpoint
    try:
        cmd = __check_address(address)
    except TypeError as e:
        print(f"[!] ERROR: {e}")
        return None

    if is_temporary:
        cmd = "t"+cmd
    try:
        gdb.execute(cmd)
        return get_breakpoints()[-1]
    except Exception as e:
        print(f"[!] ERROR: {e}")
        return None


def set_watchpoint(address: int|str, is_temporary=False, type=gdb.WP_WRITE) -> Breakpoint|None:
    """Set a watchpoint in the code given the address.

    Args:
        address (int, str): The int address or a valid string for command watch
        is_temporary (bool, optional): Whether to create a temporary breakpoint or a permanent one. Defaults to False.
        type (gdb.WP_WRITE/gdb.WP_READ/gdb.WP_ACCESS, optional): The watchpoint type. Defaults to gdb.WP_WRITE.

    Returns:
        (Breakpoint, None): The newly created watchpoint object. None if couldn't create one
    """
    return __set_general_break(address, gdb.BP_WATCHPOINT, is_temporary, wp_type=type)

def __set_general_break(address: int|str, b_type: int, is_temporary: bool, wp_type=gdb.WP_WRITE) -> Breakpoint|None:
    try:
        cmd = __check_address(address)
    except TypeError as e:
        print(f"[!] ERROR: {e}")
        return None

    try:
        if type == gdb.BP_WATCHPOINT:
            return Breakpoint(gdb.Breakpoint(cmd, type=b_type, temporary=is_temporary, wp_class=wp_type))
        else:
            return Breakpoint(gdb.Breakpoint(cmd, type=b_type, temporary=is_temporary))
    except Exception as e:
        print(f"[!] ERROR: {e}")
        return None

def __check_address(address: int|str) -> str:
    """
    Get the address to insert in the breakpoint command
    Args:
        address (int, str): The address to be checked

    Returns:
        (str): The address as a string
    """
    if isinstance(address, int):
        return f"*{hex(address)}"
    if isinstance(address, str):
        try:
            a = int(address, 16)
            return f"*{hex(address)}"
        except:
            pass
        try:
            _ = int(address, 10)
            return f"*{address}"
        except:
            pass
        
        return address
    else:
        raise TypeError("Wrong input type. The argument must be an int or a string")