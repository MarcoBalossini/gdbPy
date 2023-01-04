import gdb
import re

class Instruction():
    """Class containing instructions data
    """
    def __init__(self, address: int, offset: int, instruction: str, notes: str) -> None:
        self.address = address
        self.offset = offset
        self.instruction = instruction
        self.notes = notes

def get_architecture() -> str|None:
    """Return the file architecture's name

    Returns:
        str|None: The architecture name
    """
    try:
        return gdb.newest_frame().architecture().name()
    except Exception as e:
        print(f"[!] ERROR: {e}")

def current_function() -> str|None:
    """Return the currently executing function

    Returns:
        str|None: The current function name
    """
    try:
        return gdb.newest_frame().name()
    except Exception as e:
        print(f"[!] ERROR: {e}")

# Could be done with gdb.Architecture.disassemble()
# however it does not return the instructions offset
def disass(where: str ="") -> list[Instruction]:
    """Disassemble the current function or the given location.

    Args:
        where (str, optional): The location where to disassemble. Defaults to "".

    Returns:
        list[Instruction]: The disassembled function
    """
    dis = gdb.execute(f"disass {where}", to_string=True)
    dis = dis.split("\n")[1:-2]

    instructions = []
    for line in dis:
        m = re.match(".{3}0x([A-Fa-f0-9]+) <([+-]\d+)>:\t([^#]+)[\s]*#{0,1}\s*(.*)", line)
        address = int(m.group(1), 16)
        offset = int(m.group(2), 10)
        instruction = m.group(3)
        notes = m.group(4)
        if len(notes)>0:
            re.sub("\s+", " ", notes)
        instructions.append(Instruction(address, offset, instruction, notes))
    return instructions

def read_register(name: str) -> str|None:
    """
    Get register value
    :param str name: The register name. e.g., 'rax' or 'rsp'
    """
    try:
        return gdb.newest_frame().read_register(name)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def read_variable(name: str) -> str|None:
    """Get variable value

    Args:
        name (str): The variable name. e.g., 'rax' or 'rsp'

    Returns:
        str: The variable value
    """
    try:
        return gdb.newest_frame().read_var(name)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def backtrace(full: bool =False) -> list[dict]|None:
    """
    Show call stack

    Args:
        full (bool): Whether or not to include local variables
    
    Returns:
        list[dict]|None: The backtrace
    """
    try:
        bt = gdb.execute(f"backtrace {'full' if full else ''}", to_string=True)
        bt = bt.split("\n")
        
        bt_list = []
        for line in bt[:-1]:
            print(">", line)
            m = re.match("#(\d+)  0x([A-Fa-f0-9]+) in ([A-Za-z0-9_]+) \(\)( from (.*)){0,1}", line)
            number = int(m.group(1))
            print(number)
            address = int(m.group(2), 16)
            print(address)
            f_name = m.group(3)
            print(f_name)
            from_path = m.group(5)
            print(from_path)

            btline = {}
            btline["number"] = number
            btline["address"] = address
            btline["name"] = f_name
            btline["from"] = from_path
            bt_list.append(btline)
        return bt_list

    except Exception as e:
        print(f"[!] ERROR: {e}")

def print_memory(address: int, n_units: int, format: str ="x", unit: str ="g") -> str|None:
    """Prints raw memory from given address for n units of given type with given format

    Args:
        address (int): The starting address
        n_units (int): The number of units to display
        format (str, optional): The format of the units. Defaults to "x".
        unit (str, optional): The type of units. Defaults to "g".

    Returns:
        str: The raw memory
    """
    cmd = f"x/{n_units}{format}{unit} {address}"
    try:
        return gdb.execute(cmd, to_string=True)
    except Exception as e:
        print(f"[!] ERROR: {e}")