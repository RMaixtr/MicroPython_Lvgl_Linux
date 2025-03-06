import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
from machine import Timer
from machine import I2C
import gc

config_touchscreen_support = True
board_m1n = False

lcd.init()

TOUCH = None
DEBUG = False

state = 0
click = time.time()

def read_cb(drv, ptr):
    global state,click
    # print(ptr, "123")
    data = lv.indev_data_t.cast(ptr)
    data.point = lv.point_t({'x': 160, 'y': 120})
    if time.time() - click > 1:
        state ^= 1
        click = time.time()
    # print(state)
    data.state = lv.INDEV_STATE.PR if state else lv.INDEV_STATE.REL
    return False


lv.init()

disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1

disp_drv.flush_cb = lv_h.flush
disp_drv.hor_res = 320
disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)

if config_touchscreen_support:
    indev_drv = lv.indev_drv_t()
    lv.indev_drv_init(indev_drv)
    indev_drv.type = lv.INDEV_TYPE.POINTER
    indev_drv.read_cb = read_cb
    lv.indev_drv_register(indev_drv)

lv.log_register_print_cb(lambda level,path,line,msg: print('%s(%d): %s' % (path, line, msg)))

def event_handler(obj, event):
    global btn, box, bg
    print(123)

    # if event == lv.EVENT.CLICKED:
    #     if obj == btn:
    #         box.set_hidden(0)
    #         bg.set_hidden(0)
    #     elif obj == box:
    #         box.set_hidden(1)
    #         bg.set_hidden(1)

#create screen object
scr = lv.obj()

#create button in center with callback
btn = lv.btn(scr)
btn.align(scr, lv.ALIGN.CENTER, 0, 0)
btn.set_event_cb(event_handler)
label = lv.label(btn)
label.set_text("Press me")
label.set_size(20,20)


lv.scr_load(scr)

def on_timer(timer):
    lv.tick_inc(5)
    lv.task_handler()
    gc.collect()

timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

while True:
    pass
