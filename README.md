[![License: GPL v3](https://img.shields.io/github/license/MarcoBalossini/gdbPy)](https://www.gnu.org/licenses/gpl-3.0)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/MarcoBalossini/gdbPy/graphs/commit-activity)

# gdbPy
Not so many people are skilled in the dark arts of gdb scripting... and I'm not one of those!
gdbPy is an attempt to help all this people to write a higher level gdb scripts.<br>
gdbPy relies on GNU Python APIs for gdb to do the work, but without the need of installing gdb module on python ([more on this matter](#gdb-module-for-python))<br>
Be aware that gdbPy is still in the early phase of its development. In case some problem arises write an issue and be patient :-)

## Installation
Download the .whl file in dist folder and run the command
```bash
python3 -m pip install path/to/package.whl
```

## GDB module for Python
The major dependency (and major problem) of gdbPy is gdb module for Python: it cannot be easily installed as a normal module but, as far as I know, there's only one online [guide](http://tromey.com/blog/?p=494) (written in 2008 and never updated) to install it.<br>
In short gdb it's not a Python library, and its import will work only if it's running within the gdb process.
Fortunately gdb embeds python interpreter, so we can rerun the scripts importing gdbPy like 
```
gdb -q -x script.py
```

## Examples
```python
from gdbPy import *

set_file("exFile")

# Breakpoints
set_breakpoint("main+42")
set_breakpoint(0xdeadbeef)
set_breakpoint("*0xdeadbeef")

# Start execution
start()/run()

# Debugging actions
next_instruction()/next_instruction(repeat=2)
step_in()
countinue_exec()

# Can't find the command you need?
res = execute("command")

# Now quit gdb
quit()
```