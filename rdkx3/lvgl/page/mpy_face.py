import lvgl as lv
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("face: create")

    pm.create_page_lis(lambda val: None, "Face Registration")

    def event_cb(event):
        pm.remote_msg(f'Face Registration:{event.get_target_obj().get_selected()}'.encode())

    dd = lv.dropdown(page)
    dd.set_options("\n".join([
        pm._("Owner"),
        pm._("Family"),
        pm._("Friend"),
        pm._("Enemy")]))
    lis = dd.get_list()
    lis.set_style_text_font(pm.font, 0)
    dd.set_style_text_font(pm.font, 0)
    dd.set_symbol("∨")
    dd.align(lv.ALIGN.TOP_MID, 0, 90)
    dd.add_event_cb(event_cb, lv.EVENT.VALUE_CHANGED, None)


def unLoad(page):
    print("face: unLoad")

page = lv_pm.page(create, unLoad, descrip="face")