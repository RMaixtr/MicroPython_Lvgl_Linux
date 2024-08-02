import output_display as lv
import time
import msdev
from lv_utils import event_loop

state = False

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buf_size = width * height * 3
        self.buf1 = bytearray(self.buf_size)
        self.buf2 = bytearray(self.buf_size)

        self.disp_drv = lv.display_create(self.width, self.height)
        self.disp_drv.set_color_format(lv.COLOR_FORMAT.RGB888)
        self.disp_drv.set_buffers(self.buf1, self.buf2, self.buf_size, lv.DISPLAY_RENDER_MODE.FULL)
        self.disp_drv.set_resolution(240, 320)
        self.disp_drv.set_rotation(lv.DISPLAY_ROTATION._90)
        self.disp_drv.set_flush_cb(self.flush)

    def flush(self, disp, area, color_p):
        a = color_p

        # lv.draw_sw_rotate(color_p,a,self.width,self.height,self.height*3,self.width*3,lv.DISPLAY_ROTATION._90,lv.COLOR_FORMAT.RGB888)

        data_view = a.__dereference__(self.buf_size)

        data_bytes = bytes(data_view)

        i = 0
        while True:
            try:
                with open("/tmp/my_fifo", 'wb') as fifo:
                    fifo.write(data_bytes)
                break
            except Exception as e:
                if i >= 3:
                    break
                i += 1
        
        disp.flush_ready()



lv.init()


event_loop = event_loop()
# disp = lv.linux_fbdev_create()
# lv.linux_fbdev_set_file(disp, "/dev/fb0")
display = Display(240, 320)


mouse = msdev.mouse_indev(lv.screen_active())

btn = lv.button(lv.screen_active())
btn.set_pos(50, 50)
btn.set_size(120, 50)

label = lv.label(btn)
label.set_text("Button")
label.center()

def event_handler(evt):
    if evt.get_code() == lv.EVENT.CLICKED:
        print("Button clicked")

btn.add_event_cb(event_handler, lv.EVENT.CLICKED, None)
a = 0
b = 0
while True:
    btn.set_pos(a, b)
    a+=1
    b+=1
    if a > 300:
        a = 0
        b = 0

    time.sleep_ms(50)
