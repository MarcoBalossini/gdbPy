import gdb

def attach(process: int) -> None:
    """Attach gdb to a running process

    Args:
        process (int): The process pid
    """
    try:
        if isinstance(process, int):
            gdb.execute(f"attach {process}")
        # TODO: pwntools process object
        # 
        # else:
        #     from pwnlib.util.proc import pidof
        #     pid = pidof(process)[0]
        #     gdb.execute(f"attach {pid}")
    except Exception as e:
        print(f"[!] ERROR: {e}")
        if 'ptrace' in str(e):
            import psutil
            import os
            print("\tgdb needs the permission to attach to this process.")
            print("\tFirst make sure you're the owner of the attaching process.")
            print("\tIf it's the case you can choose one of the following options:")
            process = psutil.Process(os.getpid())

            pname = ""
            for arg in process.cmdline():
                if ".py" in arg:
                    pname = arg
                    break
            print(f"\t    1) Run again the process as a superuser: \"sudo python3 {pname}\"")
            print("\t    2) Set ptrace_scope to 0: \"sudo echo 0 > /proc/sys/kernel/yama/ptrace_scope\"")

def set_file(filename: str) -> None:
    """Sets a file in gdb, given its name

    Args:
        filename (str): The name of the file to debug
    """
    try:
        gdb.execute(f"file ./{filename}")
    except Exception as e:
        print(f"[!] ERROR: File not set. {e}")

def set_args(args: list[str]) -> None:
    """Sets the argument to the execution

    Args:
        args (list(str)): Arguments to use at the execution
    """
    try:
        cmd = "set args"
        for arg in args:
            cmd += f" {arg}"
        gdb.execute(cmd)
    except:
        print("[!] ERROR: args not set")

def execute(cmd: str) -> str|None:
    """Executes a generic command

    Args:
        cmd (str): The command

    Returns:
        str: The command result
    """
    try:
        return gdb.execute(cmd, to_string=True)
    except Exception as e:
        print(f"[!] ERROR: {e}")

def choose_thread(thread_num: int) -> None:
    """Monitor a given thread

    Args:
        thread_num (int): The thread number
    """
    try:
        gdb.execute(f"thread {thread_num}")
    except Exception as e:
        print(f"[!] ERROR: {e}")

def quit() -> None:
    """Quits and closes gdb
    """
    gdb.execute("quit")