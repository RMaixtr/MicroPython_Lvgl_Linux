import lvgl as lv
import lv_pm
pm = lv_pm.pm()

def create(page):
    print("test")
    but = lv.button(page)
    but.center()

    label = lv.label(but)
    label.set_text("HELLO")
    label.center()

    

def unLoad(page):
    print("test_unLoad: unLoad")

page = lv_pm.page(create, unLoad, descrip="test")