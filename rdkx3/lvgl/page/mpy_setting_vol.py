import lvgl as lv
import cmodule
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("setting_vol: create")

    # amixer get 'Headphone' | grep -oP '\[\d+\%\]' | sed 's/[^0-9]//g' | head -1
    rt = cmodule.rpopen("amixer get 'Headphone' | grep -oP '\[\d+\%\]' | sed 's/[^0-9]//g' | head -1")
    vol = int(rt)

    def vol_change(event):
        cmodule.rpopen("amixer set 'Headphone' " + str(pm.slider.get_value()))

    pm.create_page_lis(vol_change, "Volume")

    pm.slider = lv.slider(page)
    pm.slider.set_range(0, 45)
    pm.slider.set_pos(45, 142)
    pm.slider.set_size(150, 10)
    pm.slider.set_value(vol, lv.ANIM.ON)
    pm.slider.add_event_cb(vol_change,lv.EVENT.RELEASED,None)


def unLoad(page):
    print("setting_vol: unLoad")

page = lv_pm.page(create, unLoad, descrip="volume")