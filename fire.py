from blinkstick import blinkstick
from time import sleep, time
from math import sin
from colorsys import hsv_to_rgb

####
# fire.py by Different55 <burritosaur@protonmail.com>
# This script glows red and orange and flickers like a fire.
####

speed = 2 # Overall speed of the animation
popspeed = 4 # Speed of the flickers/pops

### END OPTIONS ###

stk = blinkstick.find_first()
cnt = stk.get_led_count()

while True:
	data = []
	for i in range(cnt):
		x = time()*speed # Base speed control
		y = x+i # For some variation from LED to LED
		z = x*popspeed+i**2 # For the sporadic flickering
		hue = ((sin(y/.4)+sin(y/.2)+sin(y/.5))/6+.5)*.06 # Main color
		hueplus = max((sin(z)+sin(z/3.0)+sin(z/7.0))/5-.4,0) # Flicker
		r, g, b = hsv_to_rgb(min(hue+hueplus, .07), 1.0-hueplus, sin(z)/8+.875) # Convert to RGB
		#print(hueplus, r, g, b)
		data = data + [int(g*255), int(r*255), int(b*255)] # Convert to GRB and add to the frame.
	stk.set_led_data(0, data) # Send off to the blinkstick
	sleep(0.02) # Nap for a bit so we don't overwhelm the blinkstick.
