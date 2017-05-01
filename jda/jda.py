# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v55.3+.
from __future__ import print_function, absolute_import, division

from cefpython3 import cefpython as cef
import platform
import sys
import subprocess

JUPYTER_COMMAND = "jupyter notebook  --port={port} --no-browser"

def is_port_free(port, host="localhost"):
    """Checks if port is open on host"""
    #based on http://stackoverflow.com/a/35370008/952600
    import socket
    from contextlib import closing

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return False
        else:
            return True

def run_jupyter(notebook_name, port=None, command=JUPYTER_COMMAND):
    """Runs a jupyter notebook server on a specified port"""
    cmd = command.format(port=port)
    print("Running command: " + cmd)
    proc = subprocess.Popen(cmd)
    print("Process PID: " + str(proc.pid))
    return proc

def main(notebook_name, port=None):
    "Run the kernel and create the browser"
    
    proc = run_jupyter(notebook_name, port)
    
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    
    cef.Initialize()
    
    url = "http://localhost:{port}/notebooks/{notebook_name}".format(notebook_name=notebook_name, port=port)
    cef.CreateBrowserSync(url=url, window_title=notebook_name)
    cef.MessageLoop()
    
    proc.terminate()
    proc.terminate()

    print("Shutting down jupyter kernel.")
    cef.Shutdown()
    proc.wait()
    


def check_versions():
    print("[hello_world.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[hello_world.py] Python {ver} {arch}".format(
          ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"


if __name__ == '__main__':
    main('example.ipynb', '14568')
