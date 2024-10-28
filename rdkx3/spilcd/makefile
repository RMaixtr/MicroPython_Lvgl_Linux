
## gcc -shared -o libspilcd.so SPILCD.c rgb2bgr.c DEV_Config.c -lwiringPi -fPIC

CC = gcc
TARGET = libspilcd.so
SOURCE = $(wildcard ./*.c) 
OBJS = $(patsubst %.c, %.o, $(SOURCE))
INCLUDE = -I./
$(TARGET):$(OBJS)
	$(CC) $(OBJS) -fPIC -lwiringPi -shared -o $(TARGET)
%.o:%.c
	$(CC) $(INCLUDE) -fPIC -lwiringPi -c $^ -o $@

.PHONY:clean
clean:
	rm $(OBJS) $(TARGET) 
