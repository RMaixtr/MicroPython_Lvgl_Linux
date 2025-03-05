
from .udpdevice import udpdevice

class rmpyc(udpdevice):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.remote = RemoteModule(self)


class RemoteModule:
    def __init__(self, client: udpdevice):
        self.__client__ = client

    def __getattr__(self, name: str):
        return RemoteAttribute(self.__client__, name)

class RemoteAttribute():
    def __init__(self, client: udpdevice, attribute_path: str):
        self.__client__ = client
        self.__attribute_path__ = attribute_path

    def __repr__(self) -> str:
        return str(self.__attribute_path__)

    def __str__(self) -> str:
        return str(self.__client__.cmd(self.__attribute_path__.encode(), add_retoutput=True))
    
    def __dir__(self):
        return self.__client__.cmd("dir(" + self.__attribute_path__ + ")".encode(), add_retoutput=True)

    def __call__(self, *args, **kwargs):
        flags = ['>', '<', 'object', 'at', '0x']
        args_repr = [repr(a) for a in args if any(
            f not in repr(a) for f in flags)]
        kwargs_repr = [f"{k}={v!r}" if not callable(
            v) else f"{k}={v.__name__}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        cmd_ = f"__remotetmp__ = {self.__attribute_path__}({signature})"
        return self.__client__.cmd(cmd_.encode())

    def __getattr__(self, name):
        return RemoteAttribute(self.__client__, f"{self.__attribute_path__}.{name}")
    
    def set(self, value):
        self.__client__.cmd(f"{self.__attribute_path__}={repr(value)}".encode())

    def get(self):
        return self.__client__.cmd(f"{self.__attribute_path__}".encode(), add_retoutput=True)

    