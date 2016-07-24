from blinkstick import blinkstick
from time import sleep
from colour import Color

stick = blinkstick.find_first()
cnt = stick.get_led_count()

wait = .05 # How long to wait between frames.

while True:
    for x in range(1,cnt+1):
        data = []
        data2 = []
        for i in range(1,cnt+1):
            if i >= x:
                data.append(64-(i*2))
                data.append(0)
                data.append(i*4)
            else:
                data2.append(64-(i*2))
                data2.append(0)
                data2.append(i*4)

        #print(data+data2)
        stick.set_led_data(0, data+data2)
        sleep(wait)
