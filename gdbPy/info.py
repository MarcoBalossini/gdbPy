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
    return gdb.newest_frame().architecture().name()

# Could be done with gdb.Architecture.disassemble()
# however it does not return the instructions offset
def disass(where="", parse=True):
    """
    Disassemble the current function or the given location.
    :param str where: The location where to disassemble
    :param bool parse: Whether to parse the output or not
    """
    dis = gdb.execute(f"disass {where}", to_string=True)
    if not parse:
        return dis

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