from . import mpy_test

import lv_pm
pm = lv_pm.pm()

# 需要保证 home 在 0
pm.add_page(mpy_test.page)