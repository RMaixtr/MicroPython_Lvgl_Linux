import lvgl as lv

path = __file__[:__file__.rfind('/')+1]

if __name__ == '__main__':
    import time
    from lv_utils import event_loop
    import fs_driver

    lv.init()
    event_loop = event_loop()
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'L')

    import drive

    import lv_pm
    pm = lv_pm.pm()
    pm.path = path
    
    import page
    pm.open_page(0)

    import rmpyc
    rmpyc.udp()
    
    while True:
        time.sleep_ms(500)
