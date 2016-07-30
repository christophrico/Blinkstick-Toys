from blinkstick import blinkstick
from time import sleep, time
from colorsys import hsv_to_rgb
from math import sin

####
# lavalamp.py by Different55 <burritosaur@protonmail.com>
# This script smoothly and slowly shifts between many colors. It's not actually
# anything like a lavalamp, it just kind of reminded me of one.
####

fps = 50.0 # FPS of the animation. 50 is about the upper limit.
speed = 1 # Speed of animation
type = 1 # "1" for hard edges on colors, "1.0" for smooth fading.
brightness = 1.0 # Brightness of animation, from 0 to 1

### END OPTIONS ###

stk = blinkstick.find_first()
cnt = stk.get_led_count()

data = [0]*96
while True:
    data = []
    for i in range(1,cnt+1):
        (r, g, b) = hsv_to_rgb((sin(time()/(8.0/speed)+i/(4*type))+1)/2, 1, brightness)
        data= data + [int(g*255), int(r*255), int(b*255)]
        #print(int(r*255), int(g*255), int(b*255))
    #print(data)
    stk.set_led_data(0, data)
    sleep(1/wait)
