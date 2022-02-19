import gdb
import re

class Instruction():
    def __init__(self, address, offset, instruction, notes) -> None:
        self.address = address
        self.offset = offset
        self.instruction = instruction
        self.notes = notes

def get_architecture():
    """Return the file architecture's name"""
    try:
        return gdb.newest_frame().architecture().name()
    except Exception as e:
        print(f"[!] ERROR: {e}")

def current_function():
    """Return the currently executing function"""
    try:
        return gdb.newest_frame().function().name
    except Exception as e:
        print(f"[!] ERROR: {e}")

# Could be done with gdb.Architecture.disassemble()
# however it does not return the instructions offset
def disass(where=""):
    """
    Disassemble the current function or the given location.
    :param str where: The location where to disassemble
    :param bool parse: Whether to parse the output or not
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

def read_register(name):
    """
    Get register value
    :param str name: The register name. e.g., 'rax' or 'rsp'
    """
    try:
        return gdb.newest_frame().read_register(name)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def read_variable(name):
    """
    Get variable value
    :param str name: The variable name. e.g., 'rax' or 'rsp'
    """
    try:
        return gdb.newest_frame().read_var(name)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def backtrace(full=False):
    """
    Show call stack
    :param bool full: Whether or not to include local variables
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