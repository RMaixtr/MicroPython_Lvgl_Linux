from cffi import FFI
ffi = FFI()
ffi.cdef("""
    void SPILCD_flush(int x1, int y1, int x2, int y2, uint8_t* color_p);
""")

ffi.cdef("""
    void SPILCD_init();
""")

fun = ffi.dlopen("./libspilcd.so")

fun.SPILCD_init()

with open("./565.bin",'rb') as file:
    data = file.read()

print(len(data))
uint8_array = ffi.new("uint8_t[]", data)

fun.SPILCD_flush(0, 0, 239, 319, uint8_array)
