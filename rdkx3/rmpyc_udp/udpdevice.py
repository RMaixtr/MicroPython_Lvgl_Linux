from typing import List, Union
from inspect import getsource
import functools
import threading
import socket

class udpdevice():
    def __init__(self, addr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", 8267))
        self.settimeout(0.2)
        self.addr = addr
        self._banner = b'\x02'
        self._kbi = b'\x03'
        self.prompt = b'>>> '
        self._traceback = b'Traceback (most recent call last):'

    def settimeout(self, sec:float):
        self.socket.settimeout(sec)

    def write(self, data:bytes):
        self.socket.sendto(data, (self.addr, 8770))

    def wait(self):
        self.ret = b""
        while True:
            try:
                data, addr = self.socket.recvfrom(65000)
            except TimeoutError:
                return self.ret
            self.ret += data
            if self.prompt in self.ret:
                break
        return self.ret

    def cmd(self, cmd:bytes, add_retoutput=False, long_string:bool = False):
        # self.socket.setblocking(False)
        # while True:
        #     try:
        #         self.socket.recvfrom(65000)
        #     except BlockingIOError:
        #         break
        # self.socket.setblocking(True)
        if add_retoutput:
            cmd = b'print(' + cmd + b')'

        # thread = threading.Thread(target=self.wait)
        # thread.start()
        self.write(cmd + b"\r")
        self.wait()
        # thread.join()
        cmd_filt = cmd + b'\r\n'
        buff = self.ret.replace(cmd_filt, b'', 1)
        if self._traceback in buff:
            long_string = True
        if long_string:
            response = buff.replace(b'\r', b'').replace(
                b'\r\n>>> ', b'').replace(b'>>> ', b'').decode()
        else:
            response = buff.replace(b'\r\n', b'').replace(
                b'\r\n>>> ', b'').replace(b'>>> ', b'').decode()
        return response
    
    def code(self, func):
        # str_func = '\n'.join(getsource(func).split('\n')[1:])
        source_lines = getsource(func).split('\n')[1:]
        indent = len(source_lines[0]) - len(source_lines[0].lstrip())
        str_func = '\n'.join([line[indent:] for line in source_lines if line.strip()])
        self.cmd(str_func.encode())

        @functools.wraps(func)
        def wrapper_cmd(*args, **kwargs):
            flags = ['>', '<', 'object', 'at', '0x']
            args_repr = [repr(a) for a in args if any(
                f not in repr(a) for f in flags)]
            kwargs_repr = [f"{k}={v!r}" if not callable(
                v) else f"{k}={v.__name__}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            cmd_ = f"{func.__name__}({signature})"
            return self.cmd(cmd_.encode())
        return wrapper_cmd
