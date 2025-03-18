import lvgl as lv
from . import lv_anim

path = __file__[:__file__.rfind('/')+1]

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

def splitpath(filename):
    filename = filename.split("/")[-1]
    parts = filename.split(".")
    if len(parts) > 1:
        return ".".join(parts[:-1]), parts[-1]
    else:
        return filename, ""

def _appear_complete_cb(pm_page, options):
    if pm_page.willAppear:
        pm_page.willAppear(pm_page.page)

def _back_appear_complete_cb(pm_page, options):
    if pm_page.didAppear:
        pm_page.didAppear(pm_page.page)

def _disAppear_complete_cb(pm_page, options):
    # todo
    if options == open_options.ANIM_NONE:
        pm_page.page.add_flag(lv.obj.FLAG.HIDDEN)
    if pm_page.willDisappear:
        pm_page.willDisappear(pm_page.page)
    # if options.open_tag == open_options.TARGET_SELF:
    pm_page.unLoad(pm_page.page)
    pm_page.page.clean()

def _back_disAppear_complete_cb(pm_page, options):
    # todo
    if options == open_options.ANIM_NONE:
        pm_page.page.add_flag(lv.obj.FLAG.HIDDEN)
    if pm_page.didDisappear:
        pm_page.didDisappear(pm_page.page)
    pm_page.unLoad(pm_page.page)
    pm_page.page.clean()


class open_options():
    ANIM_NONE = 0
    ANIM_SLIDE = 1
    ANIM_FADE = 2
    ANIM_POPUP = 3

class page():
    def __init__(self, onLoad, unLoad, descrip=None, willAppear=None, didAppear=None, willDisappear=None, didDisappear=None, returnable=True, screen = lv.screen_active()):
        screen.remove_flag(lv.obj.FLAG.SCROLLABLE)
        self.page = lv.obj(screen)
        self.page.remove_flag(lv.obj.FLAG.SCROLLABLE)
        self.page.set_style_border_width(0, lv.STATE.DEFAULT)
        self.page.set_style_radius(0, lv.STATE.DEFAULT)
        self.page.set_style_pad_all(0, lv.STATE.DEFAULT)
        self.page.add_flag(lv.obj.FLAG.HIDDEN)
        self.page.set_height(screen.get_height())
        self.page.set_width(screen.get_width())

        self.onLoad = onLoad
        self.willAppear = willAppear
        self.didAppear = didAppear
        self.willDisappear = willDisappear
        self.didDisappear = didDisappear
        self.unLoad = unLoad
        self.returnable = returnable

        self.descrip = descrip

        self.__back = False
        self.__options = None

@singleton
class pm():
    def __init__(self):
        self.history = []
        self.router = []
        # turn off the scroll bar
        lv.screen_active().set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
    
    def add_page(self, page):
        self.router.append(page)
        return len(self.router) - 1
    
    def open_page(self, id, options=open_options.ANIM_NONE):
        if (id > len(self.router) - 1) or id < 0:
            return False, "id err"
        self.history.append(id)
        pm_page = self.router[id]
        
        pm_page.__options = options
        pm_page.__back = False
        if len(self.history) > 1:
            prev_pm_page = self.router[self.history[-2]]
            prev_pm_page.__back = False
            if prev_pm_page.willDisappear:
                prev_pm_page.willDisappear(prev_pm_page.page)
            lv_anim._pm_anim_disAppear(prev_pm_page, pm_page.__options, _disAppear_complete_cb)
        pm_page.onLoad(pm_page.page)
        pm_page.page.remove_flag(lv.obj.FLAG.HIDDEN)
        pm_page.page.move_foreground()
        if pm_page.willAppear:
            pm_page.willAppear(pm_page.page)
        lv_anim._pm_anim_appear(pm_page, pm_page.__options, _appear_complete_cb)
        self.create_backbut()
    
    def back(self):
        
        pm_page = self.router[self.history.pop()]
        pm_page.__back = True
        if pm_page.willDisappear:
            pm_page.willDisappear(pm_page.page)
        lv_anim._pm_anim_disAppear(pm_page, pm_page.__options, _back_disAppear_complete_cb)

        while not self.router[self.history[-1]].returnable:
            self.history.pop()
            if len(self.history) < 1:
                return False
        prev_pm_page = self.router[self.history[-1]]
        prev_pm_page.__back = True
        if prev_pm_page.willDisappear:
            prev_pm_page.willDisappear(prev_pm_page.page)

        prev_pm_page.onLoad(prev_pm_page.page)
        prev_pm_page.page.remove_flag(lv.obj.FLAG.HIDDEN)
        prev_pm_page.page.move_foreground()
        lv_anim._pm_anim_appear(prev_pm_page, pm_page.__options, _back_appear_complete_cb)
        self.create_backbut()
        return True
    
    def back_home(self):
        pm_page = self.router[self.history.pop()]
        pm_page.__back = True
        if pm_page.willDisappear:
            pm_page.willDisappear(pm_page.page)
        lv_anim._pm_anim_disAppear(pm_page, pm_page.__options, _back_disAppear_complete_cb)

        prev_pm_page = self.router[0]
        self.history = [0]
        prev_pm_page.__back = True
        if prev_pm_page.willDisappear:
            prev_pm_page.willDisappear(prev_pm_page.page)

        prev_pm_page.onLoad(prev_pm_page.page)
        prev_pm_page.page.remove_flag(lv.obj.FLAG.HIDDEN)
        prev_pm_page.page.move_foreground()
        lv_anim._pm_anim_appear(prev_pm_page, pm_page.__options, _back_appear_complete_cb)
        return True
    
    def create_backbut(self):
        if len(self.history) > 1:
            def back_cb(event):
                if(event.get_code() == lv.EVENT.RELEASED):
                    if self.mouse.y - 5 > 70:
                        self.back()
            def back_home_cb(event):
                if(event.get_code() == lv.EVENT.RELEASED):
                    if lv.screen_active().get_height() - self.mouse.y > 70:
                        self.back_home()
            ret = lv.button(self.router[self.history[-1]].page)
            ret.set_size(240, 20)
            ret.set_style_opa(0, lv.STATE.DEFAULT)
            ret.align(lv.ALIGN.TOP_MID,0,0)
            ret.add_flag(lv.obj.FLAG.CLICKABLE)
            # ret.add_event_cb(drag_PRESS_cb,lv.EVENT.PRESSING,None)
            ret.add_event_cb(back_cb,lv.EVENT.RELEASED,None)

            ret_home = lv.button(self.router[self.history[-1]].page)
            ret_home.set_size(240, 20)
            ret_home.set_style_opa(0, lv.STATE.DEFAULT)
            ret_home.align(lv.ALIGN.TOP_MID,0,lv.screen_active().get_height()-20)
            ret_home.add_flag(lv.obj.FLAG.CLICKABLE)
            # ret_home.add_event_cb(drag_PRESS_cb,lv.EVENT.PRESSING,None)
            ret_home.add_event_cb(back_home_cb,lv.EVENT.RELEASED,None)

    def message(self, text="", caption="", type=True):
        tempcard_touched = False
        msg_panel_h = 80
        temp_card = lv.tileview(lv.layer_top())
        temp_card.set_size(200,80)
        temp_card.set_style_bg_color(lv.color_hex(0x555555), lv.PART.MAIN)
        temp_card.set_style_radius(15, lv.PART.MAIN)
        temp_card.remove_flag(lv.obj.FLAG.SCROLLABLE)
        temp_card.align(lv.ALIGN.TOP_MID, 0, -40)
        temp_card.set_style_opa(230, lv.STATE.DEFAULT)

        def tempcard_ready_cb(tempcard):
            tmp = lv.anim_t()
            tmp.init()
            tmp.set_var(tempcard)
            tmp.set_custom_exec_cb(lambda a,val: tempcard.set_y(val))
            tmp.set_path_cb(lv.anim_t.path_ease_out)
            tmp.set_completed_cb(lambda a: tempcard.delete())
            tmp.set_delay(3000)
            tmp.set_time(300)
            tmp.set_values(10, -msg_panel_h)
            tmp.start()

        click_point1 = lv.point_t()
        click_point2 = lv.point_t()
        def tempcard_press_cb(e):
            nonlocal tempcard_touched, a
            tempcard = e.get_target_obj()
            lv.anim_t.custom_delete(a, None)

            if not tempcard_touched:
                lv.indev_active().get_point(click_point1)
                tempcard_touched = True
                return
            else:
                lv.indev_active().get_point(click_point2)
            j=click_point2.y-click_point1.y
            click_point1.y=click_point2.y
            if j < 0:
                tempcard.set_y(tempcard.get_y() + j)

        def tempcard_released_cb(e):
            nonlocal tempcard_touched
            tempcard = e.get_target_obj()
            tempcard_touched = False
            tmp = lv.anim_t()
            tmp.init()
            tmp.set_var(tempcard)
            tmp.set_custom_exec_cb(lambda a,val: tempcard.set_y(val))
            tmp.set_time(200)
            if tempcard.get_y() < -msg_panel_h/3:
                tmp.set_completed_cb(lambda a: tempcard.delete())
                tmp.set_values(tempcard.get_y(), -msg_panel_h)
            else:
                tmp.set_completed_cb(lambda a: tempcard_ready_cb(tempcard))
                tmp.set_values(tempcard.get_y(), 10)
            tmp.start()

        temp_card.add_event_cb(tempcard_press_cb,lv.EVENT.PRESSING,None)
        temp_card.add_event_cb(tempcard_released_cb,lv.EVENT.RELEASED,None)
        # temp_card.add_event_cb(event_cb,lv.EVENT.SHORT_CLICKED,None)


        if type:
            with open(path + '../reset/bot.png', 'rb') as f:
                png_data = f.read()
        else:
            with open(path + '../reset/user.png', 'rb') as f:
                png_data = f.read()

        img = lv.image_dsc_t({
            "data_size": len(png_data),
            "data": png_data,
        })
        # 55*55
        msg_icon = lv.image(temp_card)
        msg_icon.set_src(img)
        msg_icon.set_pos(10,10)

        title_lable = lv.label(temp_card)
        title_lable.set_style_text_font(self.font, 0)
        title_lable.set_text(caption)
        title_lable.set_pos(80,15)
        title_lable.set_style_text_color(lv.color_hex(0xffffffff), 0)

        txt_lable = lv.label(temp_card)
        txt_lable.set_style_text_font(self.font, 0)
        txt_lable.set_text(text)
        txt_lable.set_pos(80,45)
        txt_lable.set_style_text_color(lv.color_hex(0xffffffff), 0)

        a = lv.anim_t()
        a.init()
        a.set_var(temp_card)
        a.set_custom_exec_cb(lambda a,val: temp_card.set_y(val))
        a.set_time(300)
        a.set_path_cb(lv.anim_t.path_ease_out)
        a.set_completed_cb(lambda a: tempcard_ready_cb(temp_card))
        a.set_values(-msg_panel_h,10)
        a.start()
