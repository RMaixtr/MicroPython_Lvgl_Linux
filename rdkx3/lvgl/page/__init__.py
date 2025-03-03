from . import mpy_home, mpy_language, mpy_setting_light, mpy_setting_vol, mpy_setting_bios, mpy_face

import lv_pm
pm = lv_pm.pm()

# 需要保证 home 在 0
pm.add_page(mpy_home.page)
pm.add_page(mpy_language.page)
pm.add_page(mpy_setting_light.page)
pm.add_page(mpy_setting_vol.page)
pm.add_page(mpy_setting_bios.page)
pm.add_page(mpy_face.page)