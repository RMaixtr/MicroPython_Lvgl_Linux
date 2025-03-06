import lvgl as lv
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("language: create")

    def event_cb(event):
        if pm.get_lis_index():
            pm.set_locale("zh")
        else:
            pm.set_locale()

    pm.create_page_lis(event_cb, "Language")

    pm.create_png(pm.path+'reset/none.png', "English")
    pm.create_png(pm.path+'reset/none.png', "中文简体")

    pm.create_page_end()

    # dd = lv.dropdown(page)
    # dd.set_options("\n".join([
    #     "English",
    #     "中文简体"]))
    # lis = dd.get_list()
    # lis.set_style_text_font(pm.font, 0)
    # dd.set_style_text_font(pm.font, 0)
    # dd.set_symbol("∨")
    # dd.align(lv.ALIGN.TOP_MID, 0, 90)
    # if pm.i18n.locale:
    #     dd.set_selected(1)
    # dd.add_event_cb(event_cb, lv.EVENT.VALUE_CHANGED, None)


def unLoad(page):
    print("language: unLoad")

page = lv_pm.page(create, unLoad, descrip="language")