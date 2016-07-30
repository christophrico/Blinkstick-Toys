####
# breathing.py by Different55 <burritosaur@protonmail.com>
# This script smoothly fades between two colors in a kind of breathing pattern.
# The color is set equally to all available LEDs on the first blinkstick found.
####

wait = 0.05 # Time to wait between frames. 0.02 is about the lower limit
colorin = Color('#b71500')
colorout = Color('black')

### END OPTIONS ###

from blinkstick import blinkstick
from time import sleep
from colour import Color

stk = blinkstick.find_first()
cnt = stk.get_led_count()

while True:
	mult = 0
	last = colorout
	while last.hex != colorin.hex: # For some reason if I use anything but .hex, they'll never equal the same color.
		last = Color(rgb=((last.red*5+colorin.red)/6, (last.green*5+colorin.green)/6, (last.blue*5+colorin.blue)/6))
		data = [int(last.green*255), int(last.red*255), int(last.blue*255)] * cnt
		stk.set_led_data(0, data)
		sleep(wait)
		print('breathe in', last)
	print('pause', last)
	sleep(wait*10)
	while last.hex != colorout.hex and last.luminance > .004: # For fading to black, this helps a bit since the blinkstick completely blanks out at low brightness levels.
		last = Color(rgb=((last.red*6+colorout.red)/7, (last.green*6+colorout.green)/7, (last.blue*6+colorout.blue)/7))
		data = [int(last.green*255), int(last.red*255), int(last.blue*255)] * cnt
		stk.set_led_data(0, data)
		sleep(wait)
		print('breathe out', last)