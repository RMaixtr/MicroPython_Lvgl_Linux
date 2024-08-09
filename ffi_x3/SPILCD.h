
#ifdef __cplusplus
extern "C" {
#endif

/*********************
 *      INCLUDES
 *********************/
// #ifndef LV_DRV_NO_CONF
// #ifdef LV_CONF_INCLUDE_SIMPLE
// #include "lv_drv_conf.h"
// #else
// #include "..\..\lv_drv_conf.h"
// #endif
// #endif

// #ifdef LV_LVGL_H_INCLUDE_SIMPLE
// #include "lvgl.h"
// #else
// #include "lvgl/lvgl.h"
// #endif

/**********************
 *      TYPEDEFS
 **********************/
#include <stdint.h>
#define SPILCD_HOR_RES  		240
#define SPILCD_VER_RES  		320

/**********************
 * GLOBAL PROTOTYPES
 **********************/
void SPILCD_init(void);
void SPILCD_flush(int x1,int y1,int x2,int y2,uint8_t *color_p);

/**********************
 *      MACROS
 **********************/

#ifdef __cplusplus
} /* extern "C" */
#endif
