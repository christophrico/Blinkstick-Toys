from blinkstick import blinkstick
import time, colorsys
from math import sin

from signal import signal, SIGINT
from sys import exit
####
# fireflies.py by Different55 <burritosaur@protonmail.com>
# It lights up random LEDs in a way that looks similar to fireflies at night.
####


#To allow user to turn off color with CTRL-C
def turn_off():
    sticks = blinkstick.find_all()
    for stick in sticks:
        stick.set_led_data(0, [0, 0, 0]*stick.get_led_count())

def handler(signal_received, frame):
	print("\nLater Skater")
	turn_off()
	exit(0)


########## -------- MAIN FUNCTION ------- #########
def main():
	speed = 1 # Overall speed of the animation.
	ff_speed = 5 # Speed of the fireflies.
	fps = 50.0 # FPS of the animation. 50 is about the upper limit.

	### END OPTIONS ###

	stk = blinkstick.find_first()
	cnt = stk.get_led_count()

	while True:
		data = []
		for i in range(cnt):
			x = time.time()*speed # Base speed control
			y = x+i # For a bit of random color for the flies.
			z = x*ff_speed+i**2  # Firefly speed control
			ff_glow = max((sin(z)+sin(z/3.0)+sin(z/7.0))/5-.4,0) # Flicker. Honestly with this math I just threw stuff at the wall on desmos.com to see what stuck.
			r, g, b = colorsys.hsv_to_rgb(.10+(sin(y)/32+.03125), 1.0-ff_glow*1.3, ff_glow*5) # Convert to RGB.
			#print(hueplus, r, g, b)
			data = data + [int(g*255), int(r*255), int(b*255)] # Convert to GRB and add to the frame.
		stk.set_led_data(0, data) # Send off to the blinkstick
		time.sleep(1/fps) # Nap for a bit so we don't overwhelm the blinkstick.


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
	signal(SIGINT, handler)

	print("It's lit bruv. Press CTRL-C to turn down.")
	while True:
		main()
