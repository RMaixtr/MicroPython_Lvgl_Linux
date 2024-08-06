from maix import camera, display, image


while True:
    with open("/tmp/my_fifo", 'rb') as fifo:
        while True:
            data = fifo.read()
            if data:

                if len(data) == 320*240*3:
                    display.show(image.load(data, size=(320, 240)))
                    
            else:
                break