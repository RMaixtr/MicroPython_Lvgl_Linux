import lvgl as lv
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("face: create")

    def event_cb(event):
        pm.remote_msg(f'Face Registration:{pm.get_lis_index()}'.encode())

    
    pm.create_page_lis(event_cb, "Face Registration")

    pm.create_png(pm.path+'reset/none.png', "Owner")
    pm.create_png(pm.path+'reset/none.png', "Family")
    pm.create_png(pm.path+'reset/none.png', "Friend")
    pm.create_png(pm.path+'reset/none.png', "Enemy")

    pm.create_page_end()

    # dd = lv.dropdown(page)
    # dd.set_options("\n".join([
    #     pm._("Owner"),
    #     pm._("Family"),
    #     pm._("Friend"),
    #     pm._("Enemy")]))
    # lis = dd.get_list()
    # lis.set_style_text_font(pm.font, 0)
    # dd.set_style_text_font(pm.font, 0)
    # dd.set_symbol("∨")
    # dd.align(lv.ALIGN.TOP_MID, 0, 90)
    # dd.add_event_cb(event_cb, lv.EVENT.VALUE_CHANGED, None)



def unLoad(page):
    print("face: unLoad")

page = lv_pm.page(create, unLoad, descrip="face")