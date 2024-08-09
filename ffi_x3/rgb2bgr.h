#ifndef RGB2BGR_H
#define RGB2BGR_H
#include <stdint.h>

void mktable(uint8_t *table);
void convert_image(uint8_t *image, uint8_t *table, uint32_t size);

#endif
