from blinkstick import blinkstick
from time import sleep, time
from colorsys import hsv_to_rgb
from math import sin

####
# rotatingrainbow.py by Different55 <burritosaur@protonmail.com>
# Cycles through a full spectrum of colors and rotates it around all available
# LEDs on the first channel o the first blinkstick.
####

speed = 1 # 2 is 2x speed, .5 is half speed, you get the idea.
fps = 50.0 # Frames per second of the animation. 50 is about the upper limit.
cut = 2 # how much of the spectrum to show. 1 = full spectrum, 2 = 2 full spectrums, .5 is half a spectrum.
brightness = 1.0 # Brightness of animation from 0 to 1

stk = blinkstick.find_first()
cnt = stk.get_led_count()

while True:
    data = []
    for i in range(1,cnt+1):
        (r, g, b) = hsv_to_rgb(i/float(cnt*(1.0/cut))+time()*speed, 1, brightness)
        data = data + [int(g*255), int(r*255), int(b*255)]
        #print(int(r*255), int(g*255), int(b*255), i/32.0,)
    stk.set_led_data(0, data)
    sleep(1/fps)
