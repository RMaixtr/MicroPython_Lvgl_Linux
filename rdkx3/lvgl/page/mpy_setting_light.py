import lvgl as lv
import cmodule
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("setting_light: create")

    def bl_change(event):
        pm.set_duty(100 - pm.slider.get_value())

    pm.create_page_lis(bl_change, "Brightness")

    pm.slider = lv.slider(page)
    pm.slider.set_range(30, 100)
    pm.slider.set_pos(45, 142)
    pm.slider.set_size(150, 10)
    pm.slider.set_value(100 - pm.get_duty(), lv.ANIM.ON)
    pm.slider.add_event_cb(bl_change,lv.EVENT.RELEASED,None)


def unLoad(page):
    print("setting_light: unLoad")

page = lv_pm.page(create, unLoad, descrip="light")