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

import time
import uasyncio
from lv_utils import event_loop
import fs_driver
import random

mpy.init()
lv.init()

event_loop = event_loop(freq=20, asynchronous=True)
display = Display(240, 284)

fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'L')

async def main():
    img = lv.gif(lv.screen_active())
    img.set_src( "L:./3816.gif")
    # img.align(lv.ALIGN.CENTER, -50, 0)
    # img.set_size(120, 120)

    btn = lv.button(lv.screen_active())
    btn.set_pos(50, 50)
    btn.set_size(120, 50)

    label = lv.label(btn)
    label.set_text("Button")
    label.center()

    # 创建 线 对象
    obj_line = lv.line(lv.screen_active())
    
    # 创建样式
    style = lv.style_t()
    style.init()
    style.set_line_color(lv.palette_main(lv.PALETTE.GREY))
    style.set_line_width(6)
    style.set_line_rounded(True)
    # 添加样式
    obj_line.add_style(style, 0)
    
    a = 0
    b = 0
    c = 0

    while True:

        x1=random.randint(0,240)
        y1=random.randint(0,320)
        x2=random.randint(0,240)
        y2=random.randint(0,320)
        x3=random.randint(0,240)
        y3=random.randint(0,320)
        x4=random.randint(0,240)
        y4=random.randint(0,320)
        x5=random.randint(0,240)
        y5=random.randint(0,320)
        x6=random.randint(0,240)
        y6=random.randint(0,320)
        x7=random.randint(0,240)
        y7=random.randint(0,320)
        x8=random.randint(0,240)
        y8=random.randint(0,320)
        x9=random.randint(0,240)
        y9=random.randint(0,320)
        point =  [{"x": x1, "y": y1}, {"x": x2, "y": y2}, {"x": x3, "y":y3}, {"x": x4, "y":y4}, {"x": x5, "y":y5}, {"x": x6, "y":y6}, {"x": x7, "y":y7}, {"x": x8, "y":y8}, {"x": x9, "y":y9}]
 
        obj_line.set_points(point, len(point))
 
        obj_line.center()
        
        c+=1
        img.set_pos(0, c)
        btn.set_pos(a, b)
        a+=1
        b+=1
        if c > 80:
            c = 0
        if a > 200:
            a = 0
            b = 0
        # lv.timer_handler()
        # time.sleep_ms(100)
        await uasyncio.sleep_ms(20)
        # print("dls")

uasyncio.run(main())
