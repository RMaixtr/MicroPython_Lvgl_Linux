cd /root/MicroPython_Lvgl_Linux/rdkx3/spilcd

killall micropython

# gcc -shared -o libspilcd.so SPILCD.c rgb2bgr.c DEV_Config.c -lwiringPi -fPIC
make clean
make

echo "4" > /tmp/mpyheapsize
../micropython mpy_lvgl.py
