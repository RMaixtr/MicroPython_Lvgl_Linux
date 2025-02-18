import socket
import io
import sys

import lv_pm
pm = lv_pm.pm()

import os
import re

def get_wlan0info():
    essid, signal_level = "", ""
    rt = os.popen("iwconfig wlan0")
    tmp = rt.readlines()
    if "unassociated" in tmp[0]:
        return False
    essid_pattern = r'ESSID:"(.*?)"'
    match = re.search(essid_pattern, tmp[0])
    if match:
        essid = match.group(1)

    signal_level_pattern = r'Signal level=(\d+)/100'
    match = re.search(signal_level_pattern, tmp[6])

    if match:
        signal_level = match.group(1)

    rt = os.popen("ip -4 addr show wlan0 | grep 'inet' | awk '{print $2}' | cut -d/ -f1")
    ipaddr = rt.read()[:-1]

    return [essid, signal_level, ipaddr] if all([essid, signal_level, ipaddr]) else False

def decode_addr(addr):
    tmp = tuple(addr)
    high_byte = tmp[2]
    low_byte = tmp[3]
    port = (high_byte << 8) + low_byte
    addr = str(tmp[4])+'.'+str(tmp[5])+'.'+str(tmp[6])+'.'+str(tmp[7])
    return addr, port

class ioexec(io.IOBase):
    def __init__(self):
        self.nc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = socket.getaddrinfo('0.0.0.0', 8266)[0][4]
        self.nc.bind(addr)
        self.target = socket.getaddrinfo('0.0.0.0', 8267)[0][4]
        self.public_tag = socket.getaddrinfo('239.1.1.1', 10000)[0][4]

    def write(self, buf):
        self.nc.sendto(buf, self.target)
        return len(bytes(buf))
    
    def public_msg(self, buf):
        self.nc.sendto(buf, self.public_tag)
        return len(bytes(buf))

    def read(self, n):
        data, addr = self.nc.recvfrom(102400)
        ip, _ = decode_addr(addr)
        self.target = socket.getaddrinfo(ip, 8267)[0][4]
        return data
    
udpio = ioexec()
pm.remote_msg = udpio.public_msg

def exec_print(*args, **kwargs):
    
    flags = ['>', '<', 'object', 'at', '0x']
    args_repr = [repr(a) for a in args if any(
        f not in repr(a) for f in flags)]
    kwargs_repr = [f"{k}={repr(v)}" if not callable(
        v) else f"{k}={v.__name__}" for k, v in kwargs.items()]
    signature = ", ".join(args_repr + kwargs_repr)
    udpio.write(signature.encode())

import micropython
def mpy_exec(data):
    global print
    tmp = print
    print = exec_print
    exec(data, globals(), globals())
    print = tmp
    udpio.write(b'>>> ')
    
while True:
    result = udpio.read(None)
    pm.reload_counter()
    try:
        micropython.schedule(mpy_exec, result)
    except Exception as e:
        # sys.print_exception(e, udpio)
        micropython.schedule(udpio.write, str(sys.exc_info()).encode())

