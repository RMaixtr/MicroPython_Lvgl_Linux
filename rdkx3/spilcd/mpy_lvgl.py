
import lvgl as lv

import mpy

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buf_size = width * height * 2
        self.buf1 = bytearray(self.buf_size)
        self.buf2 = bytearray(self.buf_size)

        self.disp_drv = lv.display_create(self.width, self.height)
        self.disp_drv.set_color_format(lv.COLOR_FORMAT.RGB565)
        self.disp_drv.set_buffers(self.buf1, self.buf2, self.buf_size, lv.DISPLAY_RENDER_MODE.PARTIAL)
        self.disp_drv.set_flush_cb(self.flush)

    def flush(self, disp, area, color_p):
        data_view = color_p.__dereference__(self.buf_size)
        data_bytes = bytes(data_view)
        mpy.flush(area.x1,area.y1,area.x2,area.y2,data_bytes)

        disp.flush_ready()

import time, os
import uasyncio
from lv_utils import event_loop
import fs_driver
import random

lv_fps = 15
lv_tms = 5000 // lv_fps

mpy.init()
lv.init()

event_loop = event_loop(freq=lv_fps, asynchronous=True)

display = Display(240, 284)

fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'L')

async def main():
    global lv_tms, lv_fps

    img = lv.gif(lv.screen_active())
    img.set_src( "L:./giphy.gif")

    while True:
        mpy.set_pwm(50)
        await uasyncio.sleep_ms(lv_tms)
        mpy.set_pwm(100)
        await uasyncio.sleep_ms(lv_tms)

uasyncio.run(main())
