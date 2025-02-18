from . import mpy_aifunc,mpy_home,mpy_more,mpy_setting,mpy_setting_bios,mpy_setting_vol

import lv_pm
pm = lv_pm.pm()

# 需要保证 home 在 0
pm.add_page(mpy_home.page)
pm.add_page(mpy_more.page)
pm.add_page(mpy_setting.page)
pm.add_page(mpy_aifunc.page)
pm.add_page(mpy_setting_vol.page)
pm.add_page(mpy_setting_bios.page)