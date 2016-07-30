####
# single.py by Different55 <burritosaur@protonmail.com>
# Sets a single LED to a single color. LED is specified on the command line:
# $ python single.py 5
# This would set the 5th LED to the color, turn off all other LEDs, and exit.
####

color = [255, 255, 255] # GRB format

### END OPTIONS ###

from blinkstick import blinkstick
import sys

stick = blinkstick.find_first()
count = stick.get_led_count()

led = int(sys.argv[1])-1

if led < 0 or led > count:
	print('Make sure you got the number of LEDs right. Counting starts from 1 and can\'t go above', count, 'which is the number of LEDs on your first blinkstick')
else:
	data = [0]*led*3 + color + [0]*(count-led-1)*3
	stick.set_led_data(0, data)