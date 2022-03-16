import gdb

def handle_signal(signal, print=None, stop=None, to_pass=None):
    """Set handle options for a given signal

    Args:
        signal (str): The signal to handle
        print (bool, optional): Whether to print or not. Defaults to None.
        stop (bool, optional): Whether to stop or not. Defaults to None.
        to_pass (bool, optional): Whether to pass or not. Defaults to None.
    """
    
    if not isinstance(signal, str):
        print(f"[!] ERROR: signal must be a string.")
        return
    cmd = f"handle {signal}"

    if print!= None:
        if print:
            cmd += " print"
        else:
            cmd += " noprint"
    if stop!= None:
        if stop:
            cmd += " stop"
        else:
            cmd += " nostop"
    if to_pass!= None:
        if to_pass:
            cmd += " pass"
        else:
            cmd += " nopass"

    try:
        gdb.execute(cmd)
    except Exception as e:
        print(f"[!] ERROR: {e}")

# TODO: implement event handling with Python functions