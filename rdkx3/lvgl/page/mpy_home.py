import lvgl as lv
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("home: create")

    def img_event_cb(event):
        descrip = pm.get_lis_descrip()
        if descrip in pm.page_descrip_dict:
            pm.open_page(descrip)
        else:
            pm.remote_msg(f'clicked:{descrip}'.encode())

    pm.create_page_lis(img_event_cb, "home")

    pm.create_png(pm.path+'reset/home/info.png', "System Information")
    pm.create_png(pm.path+'reset/home/face.png', "Face Registration")
    pm.create_png(pm.path+'reset/home/network.png', "Network")
    pm.create_png(pm.path+'reset/home/status.png', "Autonomy Status")
    pm.create_png(pm.path+'reset/home/light.png', "Brightness")
    pm.create_png(pm.path+'reset/home/volume.png', "Volume")
    pm.create_png(pm.path+'reset/home/language.png', "Language")
    pm.create_png(pm.path+'reset/home/shutdown.png', "Turn off")

    pm.create_page_end()

def unLoad(page):
    print("home: unLoad")

page = lv_pm.page(create, unLoad, descrip="home")