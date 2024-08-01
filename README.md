# 一. Display interface（显示接口）

### 1. framebuffer

```python
# A simple test for Linux Frame Buffer
# Registers FB display and mouse evdev and shows line cursor
# then shows a button on screen.

import lvgl as lv
from lv_utils import event_loop
import evdev

lv.init()

# Register FB display driver

event_loop = event_loop()
disp = lv.linux_fbdev_create()
lv.linux_fbdev_set_file(disp, "/dev/fb0")

# Create a screen and a button

btn = lv.button(lv.screen_active())
btn.align(lv.ALIGN.CENTER, 0, 0)
label = lv.label(btn)
label.set_text("Hello World!")
```

### 2.通过命名管道传出，交由其他程序处理

`/tmp/my_fifo` 通过 `mkfifo` 命令生成

```python
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
        self.disp_drv.set_flush_cb(self.flush)

    def flush(self, disp, area, color_p):
        data_view = color_p.__dereference__(self.buf_size)

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
```

使用 maixpy3 显示

```python
#!/usr/bin/python3 
from maix import camera, display, image

while True:
    with open("/tmp/my_fifo", 'rb') as fifo:
        while True:
            data = fifo.read()
            if data:
                if len(data) == 320*240*3:
                    display.show(image.load(data, size=(320, 240)))
            else:
                break
```

# 二. Input device interface（输入设备接口）

### 1. 鼠标

```python
# LVGL indev driver for evdev mouse device
# (for the unix micropython port)

import ustruct
import select
import lvgl as lv

# Default crosshair cursor
class crosshair_cursor:
    def __init__(self, scr=None):
        self.scr = scr if scr else lv.scr_act()
        self.hor_res = self.scr.get_width()
        self.ver_res = self.scr.get_height()
        self.cursor_style = lv.style_t()
        self.cursor_style.set_line_width(1)
        self.cursor_style.set_line_dash_gap(5)
        self.cursor_style.set_line_dash_width(1)
        self.cursor_hor = lv.line(self.scr)
        self.cursor_hor.add_style(self.cursor_style, lv.PART.MAIN)
        self.cursor_ver = lv.line(self.scr)
        self.cursor_ver.add_style(self.cursor_style, lv.PART.MAIN)

    def __call__(self, data):
        # print("%d : %d:%d" % (data.state, data.point.x, data.point.y))
        self.cursor_hor.set_points([{'x':0,'y':data.point.y},{'x':self.hor_res,'y':data.point.y}],2)
        self.cursor_ver.set_points([{'y':0,'x':data.point.x},{'y':self.ver_res,'x':data.point.x}],2)

    def delete(self):
        self.cursor_hor.delete()
        self.cursor_ver.delete()

# evdev driver for mouse
class mouse_indev:
    def __init__(self, scr=None, cursor=None, device='/dev/input/event1'):

        # Open evdev and initialize members
        self.evdev = open(device, 'rb')
        self.poll = select.poll()
        self.poll.register(self.evdev.fileno())
        self.scr = scr if scr else lv.scr_act()
        self.cursor = cursor if cursor else crosshair_cursor(self.scr)
        self.hor_res = self.scr.get_width()
        self.ver_res = self.scr.get_height()

        # Register LVGL indev driver
        self.indev = lv.indev_create()
        self.indev.set_type(lv.INDEV_TYPE.POINTER)
        self.indev.set_read_cb(self.mouse_read)
        self.timer = self.indev.get_read_timer()
        self.timer.set_period(5)
        self.x = 0
        self.y = 0
        self.b = 0

    def mouse_read(self, indev, data) -> int:
        # Check if there is input to be read from evdev
        if not self.poll.poll()[0][1] & select.POLLIN:

            return 0

        # Read and parse evdev mouse data
        a = self.evdev.read(16)
        mouse_data = ustruct.unpack('LLHHI',a)
        if mouse_data[2] == 1:
            if mouse_data[3] == 272:
                self.b = mouse_data[4]
                self.x = 0
                self.y = 0
        elif mouse_data[2] == 2:
            if mouse_data[3] == 0:
                if mouse_data[4] < 10:
                    self.x = mouse_data[4]
                else:
                    self.x = -1
                self.y = 0
            elif mouse_data[3] == 1:
                if mouse_data[4] < 10:
                    self.y = -mouse_data[4]
                else:
                    self.y = 1
                self.x = 0

        # Data is relative, update coordinates
        data.point.x += self.x
        data.point.y -= self.y
        # Handle coordinate overflow cases
        data.point.x = min(data.point.x, self.hor_res - 1)
        data.point.y = min(data.point.y, self.ver_res - 1)
        data.point.x = max(data.point.x, 0)
        data.point.y = max(data.point.y, 0)

        # Update "pressed" status
        data.state = lv.INDEV_STATE.PRESSED if ((self.b & 1) == 1) else lv.INDEV_STATE.RELEASED

        # Draw cursor, if needed
        if self.cursor: self.cursor(data)
        return 0

    def delete(self):
        self.evdev.close()
        if self.cursor and hasattr(self.cursor, 'delete'):
            self.cursor.delete()
        self.indev.enable(False)

```

```Python
    self.timer = self.indev.get_read_timer()
    self.timer.set_period(5)
```

用于缩短 `read_cb(self.mouse_read)` 的间隔，

```Python
while True:
    lv.timer_handler()
    time.sleep_us(5000)
```

主程序中需调用 `lv.timer_handler()`

# 三. Fonts（字体）

[字体转换](https://lvgl.io/tools/fontconverter)

```Python
import lvgl as lv
from lv_utils import event_loop
import fs_driver
import time
lv.init()

# Register FB display driver

event_loop = event_loop()
disp = lv.linux_fbdev_create()
lv.linux_fbdev_set_file(disp, "/dev/fb0")

fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'L')

btn = lv.button(lv.screen_active())
btn.align(lv.ALIGN.CENTER, 0, 0)

myfont_cn = lv.binfont_create('L:/root/alibaba.bin')
label = lv.label(btn)
label.set_style_text_font(myfont_cn, 0)
label.set_text("你好")

img = lv.gif(lv.screen_active())
img.set_src( "L:/root/astronaut_ezgif.gif")
img.align(lv.ALIGN.CENTER, -50, 0)

while True:
    lv.timer_handler()
    time.sleep_us(5000)
```