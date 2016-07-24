from blinkstick import blinkstick
from time import sleep, time
from colorsys import hsv_to_rgb
from math import sin

stk = blinkstick.find_first()
cnt = stk.get_led_count()

speed = 1 # 1 is 1x speed, 0 is stopped, you get the idea
wait = 0.02 # how long to wait between sending data. 0.02 is about the lower limit.
cut = 2 # how much of the spectrum to show. 1 = full spectrum, 2 = 2 full spectrums, .5 is half a spectrum. good for devices with few LEDs.

data = [0]*96
while True:
    data = []
    for i in range(1,cnt+1):
        (r, g, b) = hsv_to_rgb(i/float(cnt*(1.0/cut))+time()*speed, 1, 1)
        data = data + [int(g*255), int(r*255), int(b*255)]
        #print(int(r*255), int(g*255), int(b*255), i/32.0,)
    #print(data)
    stk.set_led_data(0, data)
    sleep(wait)