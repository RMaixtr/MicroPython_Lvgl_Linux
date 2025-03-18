import asyncio
from typing import List, Union
from inspect import getsource
import functools

class udpdevice():
    def __init__(self, addr=b'0.0.0.0'):
        self.prompt = b'>>> '
        self._traceback = b'Traceback (most recent call last):'
        self.msg = b''
        self.addr = addr

    async def init(self):
        class UdpServerProtocol:
            def connection_made(self, transport):
                self.transport = transport

        def datagram_received(data, addr):
            self.msg += data

        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UdpServerProtocol(),
            local_addr=("0.0.0.0", 0))
        
        self.transport = transport
        protocol.datagram_received = datagram_received

        # local_addr = self.transport.get_extra_info('sockname')
        # print(f"Bound to {local_addr[0]}:{local_addr[1]}")

    def write(self, data:bytes):
        self.transport.sendto(data ,(self.addr, 8770))

    async def wait(self):
        while True:
            await asyncio.sleep(0.02)
            if self.prompt in self.msg:
                break
        return self.msg

    async def cmd(self, cmd:bytes, timeout:Union[float, None]=None, waitret=True, add_retoutput=False, long_string:bool = False):

        if add_retoutput:
            cmd = b'print(' + cmd + b')'
        self.msg = b''
        if not waitret:
            self.write(cmd + b"\r")
        else: 
            self.write(cmd + b"\r")
            await self.wait()
            cmd_filt = cmd + b'\r\n'
            buff = self.msg.replace(cmd_filt, b'', 1)
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
        init = False

        @functools.wraps(func)
        async def wrapper_cmd(*args, **kwargs):
            nonlocal init
            if not init:
                init = True
                await self.cmd(str_func.encode())
            flags = ['>', '<', 'object', 'at', '0x']
            args_repr = [repr(a) for a in args if any(
                f not in repr(a) for f in flags)]
            kwargs_repr = [f"{k}={v!r}" if not callable(
                v) else f"{k}={v.__name__}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            cmd_ = f"{func.__name__}({signature})".encode()
            return await self.cmd(cmd_)
        return wrapper_cmd
