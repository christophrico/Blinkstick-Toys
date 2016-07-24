from blinkstick import blinkstick
from time import sleep, time
from colorsys import hsv_to_rgb
from math import sin

stk = blinkstick.find_first()
cnt = stk.get_led_count()

wait = 0.02 # Time to wait between frames. 0.02 is about the lower limit
speed = 1 # Speed of animation
type = 1 # "1" for hard edges on colors, "1.0" for smooth fading.

data = [0]*96
while True:
    data = []
    for i in range(1,cnt+1):
        (r, g, b) = hsv_to_rgb((sin(time()/(8.0/speed)+i/(4*type))+1)/2, 1, 1)
        data= data + [int(g*255), int(r*255), int(b*255)]
        #print(int(r*255), int(g*255), int(b*255))
    #print(data)
    stk.set_led_data(0, data)
    sleep(wait)