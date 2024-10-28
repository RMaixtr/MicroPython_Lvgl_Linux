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


if __name__ == '__main__':
    import time
    from lv_utils import event_loop
    import fs_driver
    mpy.init()
    lv.init()

    event_loop = event_loop()
    display = Display(240, 320)

    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'L')

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
    
    a = 0
    b = 0
    while True:
        btn.set_pos(a, b)
        a+=1
        b+=1
        if a > 200:
            a = 0
            b = 0
        lv.timer_handler()
        # time.sleep_ms(1)
