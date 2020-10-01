from blinkstick import blinkstick
import time, math, collections, random, sys

from signal import signal, SIGINT
from sys import exit
####
# storm.py by Different55 <burritosaur@protonmail.com>
# Draws stormy weather. Originally built for snow, now handles rain as well.
# Lightning is coming "soon".
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
	loop = True # Whether or not the blinkstick loops around on itself. If True, flakes/drops will fall from both ends to the center of the strip.
	rotate = -4 # How much to rotate the animation. On devices like the Flex this lets you put the "top" anywhere along the strip, instead of both ends. They'll fall towards the opposite side of the strip.
	snow = True # Whether it's snowing or raining
	lightning = False # Currently not implemented.
	lightning_freq = 120
	fps = 50.0 # How many frames per second. 50 is about the upper limit. Any faster and you'll overwhelm the blinkstick.

	for arg in sys.argv:
		if arg == 'rain':
			snow = False
		elif arg == 'snow':
			snow = True

	if snow: # Snow settings
		r = 220
		g = 240
		b = 255
		speed = 1 # Speed of animation
		freq = 25 # How often spawning cycles are in frames.
		odds = 3 # How likely (1/X) a flake will spawn during a cycle.
		low_speed = 1.2 # Lower speed limit
		high_speed = 2.0 # Upper speed limit
	else: # Rain settings
		r = 40
		g = 110
		b = 180
		speed = 10
		freq = 6
		odds = 2
		low_speed = 2.1
		high_speed = 2.2

	### END OPTIONS ###

	stk = blinkstick.find_first()
	cnt = stk.get_led_count()

	flakes = []

	class Flake:
		def __init__(self, headstart = False):
			self.position = random.randint(0, 1) # Left or right
			self.speed = random.uniform(low_speed, high_speed) # How fast it falls
			if headstart:
				self.born = time.time()-random.uniform(.3, 6.0)
			else:
				self.born = time.time() # When it was created.

	flakes = flakes + [Flake(True), Flake(True), Flake(True), Flake(True), Flake(True)] # Start off with a few flakes with a headstart.
	counter = 0
	last_strike = 0

	while True:
		if loop:
			dat1 = [0]*int(cnt/2)*3
			dat2 = [0]*int(cnt/2)*3
		else:
			dat1 = [0]*cnt*3

		for i, flake in enumerate(flakes):

			position = (time.time()-flake.born)*flake.speed*speed
			if (position > cnt/2 and loop) or position > cnt:
				del flakes[i]
				continue

			f_pos = position-math.floor(position)
			led1_val = 1-f_pos
			led2_val = f_pos
			led = math.floor(position)

			try:
				if flake.position == 0 or not loop:
					dat1[led*3] = min(int(g*led1_val)+dat1[led*3], 255)
					dat1[led*3+1] = min(int(r*led1_val)+dat1[led*3+1], 255) # I wonder if I could use slices to condense this.
					dat1[led*3+2] = min(int(b*led1_val)+dat1[led*3+2], 255)

					dat1[led*3+3] = min(int(g*led2_val)+dat1[led*3+3], 255)
					dat1[led*3+4] = min(int(r*led2_val)+dat1[led*3+4], 255)
					dat1[led*3+5] = min(int(b*led2_val)+dat1[led*3+5], 255)
				else:
					led = int(cnt/2)-led
					dat2[led*3+3] = min(int(g*led1_val)+dat2[led*3+3], 255)
					dat2[led*3+4] = min(int(r*led1_val)+dat2[led*3+4], 255)
					dat2[led*3+5] = min(int(b*led1_val)+dat2[led*3+5], 255)

					dat2[led*3] = min(int(g*led2_val)+dat2[led*3], 255)
					dat2[led*3+1] = min(int(r*led2_val)+dat2[led*3+1], 255)
					dat2[led*3+2] = min(int(b*led2_val)+dat2[led*3+2], 255)
			except IndexError:
				pass

		if loop:
			data = collections.deque(dat1 + dat2)
			data.rotate(rotate*3)
		else:
			data = dat1

		stk.set_led_data(0, data) # Send off to the blinkstick
		time.sleep(1/fps) # Nap for a bit so we don't overwhelm the blinkstick.

		counter = counter + 1

		if counter % freq == 0 and random.randint(1,odds) == 1:
			flakes = flakes + [Flake()]

		if lightning and (counter % lightning_freq == 0 and random.randint(0, 2)) or (time.time()-last_strike < 1 and time.time()-last_strike > .12 and random.randint(0, 50)):
			last_strike = time.time()


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
	signal(SIGINT, handler)

	print("It's lit bruv. Press CTRL-C to turn down.")
	while True:
		main()
