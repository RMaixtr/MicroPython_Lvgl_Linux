# A simple test for Linux Frame Buffer
# Registers FB display and mouse evdev and shows line cursor
# then shows a button on screen.

import output_display as lv
from lv_utils import event_loop
import fs_driver
import time
import msdev
lv.init()

# Register FB display driver

event_loop = event_loop()
disp = lv.linux_fbdev_create()
lv.linux_fbdev_set_file(disp, "/dev/fb0")

# Register mouse device and crosshair cursor

mouse = msdev.mouse_indev(lv.screen_active(),device='/dev/input/event1')

panel = lv.obj(lv.screen_active())
panel.set_size(240, 120)
panel.set_scroll_snap_x(lv.SCROLL_SNAP.CENTER)
panel.set_flex_flow(lv.FLEX_FLOW.ROW)
panel.align(lv.ALIGN.CENTER, 0, 20)

for i in range(5):
    but = lv.button(panel)
    but.set_size(150, lv.pct(100))
    lab = lv.label(but)
    lab.set_text("Button " + str(i + 1))

    lab.align(lv.ALIGN.CENTER, 0, 0)
panel.move_to_index(0)
panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
panel.update_snap(lv.ANIM.ON)

while True:
    lv.timer_handler()
    time.sleep_us(5000)