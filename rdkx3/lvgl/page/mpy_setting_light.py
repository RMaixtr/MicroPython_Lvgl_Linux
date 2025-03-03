import lvgl as lv
import cmodule
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("setting_light: create")

    pm.create_page_lis(lambda val: None, "Brightness")

    def bl_change(event):
        if(event.get_code() == lv.EVENT.RELEASED):
            pm.set_duty(100 - event.get_target_obj().get_value())

    slider = lv.slider(page)
    slider.set_range(30, 100)
    slider.set_pos(45, 142)
    slider.set_size(150, 10)
    slider.set_value(100 - pm.get_duty(), lv.ANIM.ON)
    slider.add_event_cb(bl_change,lv.EVENT.RELEASED,None)


def unLoad(page):
    print("setting_light: unLoad")

page = lv_pm.page(create, unLoad, descrip="light")