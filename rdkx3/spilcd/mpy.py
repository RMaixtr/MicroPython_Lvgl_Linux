import ffi
libc = ffi.open("./libspilcd.so")

SPILCD_flush = libc.func("v", "SPILCD_flush", "iiiiP")
SPILCD_init = libc.func("i", "SPILCD_init", "")
SPILCD_blwrite = libc.func("v", "DEV_BLPWM_Write", "i")
SPILCD_blread = libc.func("f", "DEV_BLPWM_Read", "")

def init():
    SPILCD_init()

def flush(x1,y1,x2,y2,data):
    SPILCD_flush(x1, y1, x2, y2, data)

def set_pwm(high_edge_time):
    SPILCD_blwrite(high_edge_time)

def get_pwm():
    print(SPILCD_blread())