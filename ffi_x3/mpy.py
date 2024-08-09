import ffi
libc = ffi.open("./libtest.so")

SPILCD_flush = libc.func("v", "SPILCD_flush", "iiiiP")
SPILCD_init = libc.func("i", "SPILCD_init", "")

def init():
    SPILCD_init()

def flush(x1,y1,x2,y2,data):
    SPILCD_flush(x1, y1, x2, y2, data)