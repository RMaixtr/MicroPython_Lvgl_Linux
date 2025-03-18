import unats as nats
import io
import sys

import lv_pm
pm = lv_pm.pm()

import re
import os

def get_wlan0info():
    essid, signal_level = "", ""
    rt = os.popen("iwconfig wlan0")
    try:
        tmp = rt.split("\n")
        if "unassociated" in tmp[0]:
            return False
        essid_pattern = r'ESSID:"(.*?)"'
        match = re.search(essid_pattern, tmp[0])
        if match:
            essid = match.group(1)

        signal_level_pattern = r'Signal level=(\d+)/100'
        match = re.search(signal_level_pattern, tmp[6])
    except:
        return False

    if match:
        signal_level = match.group(1)

    rt = os.popen("ip -4 addr show wlan0 | grep 'inet' | awk '{print $2}' | cut -d/ -f1")
    ipaddr = rt[:-1]
    return [essid, signal_level, ipaddr] if all([essid, signal_level, ipaddr]) else False

class ioexec(io.IOBase):
    def __init__(self):
        self.nc = nats.connect("127.0.0.1")
        self.sub = self.nc.subscribe(b"mpy.repl.input")
        self.datalis = []

    def write(self, buf):
        self.nc.publish(b"mpy.repl.output", buf)
        return len(bytes(buf))

    def public_msg(self, buf):
        self.nc.publish(b"mpy.repl.callback", buf)
        return len(bytes(buf))

    def read(self, n):
        return self.sub.next_msg().__next__()
    
natsio = ioexec()

pm.remote_msg = natsio.public_msg

def exec_print(*args, **kwargs):
    
    flags = ['>', '<', 'object', 'at', '0x']
    args_repr = [repr(a) for a in args if any(
        f not in repr(a) for f in flags)]
    kwargs_repr = [f"{k}={repr(v)}" if not callable(
        v) else f"{k}={v.__name__}" for k, v in kwargs.items()]
    signature = ", ".join(args_repr + kwargs_repr)
    natsio.write(signature.encode())

import micropython
def mpy_exec(data):
    global print
    tmp = print
    print = exec_print
    exec(data, globals(), globals())
    print = tmp
    natsio.write(b'>>> ')
    
while True:
    result = natsio.read(None)
    tmp = result.data

    if result.subject == b'mpy.repl.input':
        try:
            micropython.schedule(mpy_exec, tmp)
        except Exception as e:
            # sys.print_exception(e, natsio)
            natsio.write(str(sys.exc_info()).encode())
