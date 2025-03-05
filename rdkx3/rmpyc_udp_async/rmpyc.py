
from .udpdevice import udpdevice

class rmpyc(udpdevice):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.remote = RemoteModule(self)


class RemoteModule:
    def __init__(self, client: rmpyc):
        self.__client__ = client

    def __getattr__(self, name: str):
        return RemoteAttribute(self.__client__, name)
    

class RemoteAttribute():
    def __init__(self, client: rmpyc, attribute_path: str):
        self.__client__ = client
        self.__attribute_path__ = attribute_path

    def __repr__(self) -> str:
        return str(self.__attribute_path__)

    async def str(self):
        return await self.__client__.cmd(self.__attribute_path__.encode(), add_retoutput=True)
    
    async def dir(self):
        return await self.__client__.cmd(("dir(" + self.__attribute_path__ + ")").encode(), add_retoutput=True)

    async def __call__(self, *args, **kwargs):
        flags = ['>', '<', 'object', 'at', '0x']
        args_repr = [repr(a) for a in args if any(
            f not in repr(a) for f in flags)]
        kwargs_repr = [f"{k}={v!r}" if not callable(
            v) else f"{k}={v.__name__}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        # cmd_ = f"{ret.__attribute_path__ if ret else '__remotetmp__'} = {self.__attribute_path__}({signature})"
        cmd_ = f"__remotetmp__ = {self.__attribute_path__}({signature})"
        return await self.__client__.cmd(cmd_.encode(), waitret=True)

    def __getattr__(self, name):
        return RemoteAttribute(self.__client__, f"{self.__attribute_path__}.{name}")
    
    async def set(self, value):
        await self.__client__.cmd(f"{self.__attribute_path__}={repr(value)}".encode())

    async def get(self):
        return await self.__client__.cmd(f"{self.__attribute_path__}".encode(), add_retoutput=True)

