#include "rgb2bgr.h"


void mktable(uint8_t *table) {
    for (uint32_t i = 0; i != 65536; i++) {
        uint16_t bgr565 = ((i & 0x1F) << 11) |
                      (((i >> 5) & 0x3F) << 5) |
                      ((i >> 11) & 0x1F);
        *table++ = bgr565 ;
        *table++ = (bgr565 >> 8) ;
    }
}

void convert_image(uint8_t *image, uint8_t *table, uint32_t size) {
    uint8_t* index;
    for (uint32_t i = 0; i != size; i+=1) {
        index = table + ((*(image + 1) << 8) | *image)*2;
        *(image++) = *(index+1);
        *(image++) = *(index);
    }
}
