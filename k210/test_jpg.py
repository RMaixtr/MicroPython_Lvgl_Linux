
# init


import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
import ustruct as struct
from machine import Timer
import image

lcd.init()
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


# lv.log_register_print_cb(lv_h.log)
lv.log_register_print_cb(lambda level,path,line,msg: print('%s(%d): %s' % (path, line, msg)))

snapshot = image.Image("/flash/1.jpg")

# Create a screen with a draggable image

scr = lv.obj()
img = lv.img(scr)
img_data = snapshot.to_bytes()
# img.align(scr, lv.ALIGN.CENTER, 0, 0)
img_dsc = lv.img_dsc_t({
    'header':{
        'always_zero': 0,
        'w':snapshot.width(),
        'h':snapshot.height(),
        'cf':lv.img.CF.TRUE_COLOR
    },
    'data_size': len(img_data),
    'data': img_data
})

img.set_src(img_dsc)
img.set_drag(True)

# # Load the screen and display image


lv.scr_load(scr)

def on_timer(timer):
    lv.tick_inc(5)
    lv.task_handler()
    # print("tick")
	
timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

i = 1
update_tim = time.ticks_ms()
def show_image(timer):
    global i,update_tim
    # # if i >1 :
    # return


# timer = Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=50, unit=Timer.UNIT_MS, callback=show_image, arg=None)


while True:
    run_tim = time.ticks_ms()
    snapshot = image.Image("/flash/"+str(i)+".jpg")
    i = i + 1 if i < 30 else 1
    img_data = snapshot.to_bytes()
    # img.align(scr, lv.ALIGN.CENTER, 0, 0)
    img_dsc = lv.img_dsc_t({
        'header':{
            'always_zero': 0,
            'w':snapshot.width(),
            'h':snapshot.height(),
            'cf':lv.img.CF.TRUE_COLOR
        },
        'data_size': len(img_data),
        'data': img_data
    })

    img.set_src(img_dsc)
    img.set_drag(True)
    print("show image", i,len(img_data),time.ticks_ms()- update_tim,time.ticks_ms()- run_tim)
    update_tim = time.ticks_ms()