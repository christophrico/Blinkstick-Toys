from blinkstick import blinkstick
import time, math, collections, random, colorsys

from signal import signal, SIGINT
from sys import exit
####
# stars.py by Different55 <burritosaur@protonmail.com>
# Imitates a night sky with occasional shooting stars.
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
	fps = 50 # How many frames per second. 50 is about the upper limit. Any faster and you'll overwhelm the blinkstick.
	speed = 50 # Speed of animation
	freq = 200 # How often shooting stars spawn
	odds = 4 # How likely (1/X) a shooting star will spawn during a cycle.
	trail = 3 # How long a shooting's star trail is. Currently not implelemented.
	loop = True # Whether or not this blinkstick is arranged with its LEDs in a loop, like a Flex taped end to end. Or not taped end to end. For this script if you have more than a few LEDs it's pretty well recommended to have this on.
	rotate = -3 # How much to rotate the animation. On devices like the Flex this lets you put the "top" anywhere along the strip. Shooting stars will fall towards the opposite point on the strip. By default the fall from both ends of the strip towards the middle.

	## END OF OPTIONS ##

	stk = blinkstick.find_first()
	cnt = stk.get_led_count()

	class ShootingStar:
		def __init__(self):
			if loop:
				self.position = random.randint(0, 1) # Left or right side
			else:
				self.position = 0
			self.speed = speed # How fast it falls
			headstart = max(random.uniform(-.3,0.3), 0)
			self.born = time.time()-headstart
			self.lifespan = random.uniform(headstart+.2, headstart+.6)

	def generate_stars(cnt): # Generate a night sky full of stars
		sky = []
		last = -999
		for i in range(cnt):
			if random.randint(0,3) == 0 and i-last > 1:
				r, g, b = colorsys.hsv_to_rgb(0.09, random.uniform(.1, .25), random.uniform(.3, .55))
				if random.randint(0,1) == 0:
					sky = sky+[int(g*255),int(r*255),int(b*255)] # reddish star
				else:
					sky = sky+[int(g*255),int(b*255),int(r*255)] # bluish star
				last = i
			else:
				sky = sky+[0,0,0]
		return sky

	stars = []

	idata = generate_stars(cnt) # This is basically an initial picture of the sky.

	counter = 0

	while True:
		if loop:
			dat1 = idata[:int(cnt/2)*3]
			dat2 = idata[int(cnt/2)*3:]
		else:
			dat1 = idata[:] # This slice grabs the whole thing. If we don't use slices, the two just link to the same list and we can't have that.

		if len(stars) > 0:
			for i, star in enumerate(stars):
				position = (time.time()-star.born)*star.speed
				if (position > cnt/2 and loop) or (position > cnt and not loop) or time.time()-star.born > star.lifespan:
					del stars[i]

				f_pos = position-math.floor(position)
				led1_val = 1-f_pos
				led2_val = f_pos
				led = math.floor(position)

				try:
					if star.position == 0:
						dat1[led*3] = max(int(100*led1_val), dat1[led*3])
						dat1[led*3+1] = max(int(105*led1_val), dat1[led*3+1]) # I wonder if I could use slices to condense this.
						dat1[led*3+2] = max(int(95*led1_val), dat1[led*3+2])

						dat1[led*3+3] = max(int(100*led2_val), dat1[led*3+3]) # This one's green
						dat1[led*3+4] = max(int(105*led2_val), dat1[led*3+4]) # Red
						dat1[led*3+5] = max(int(95*led2_val), dat1[led*3+5])  # and blue. Same pattern for the rest of them.
						pass
					else:
						led = int(cnt/2)-led
						dat2[led*3+3] = max(int(100*led1_val), dat2[led*3+3])
						dat2[led*3+4] = max(int(105*led1_val), dat2[led*3+4])
						dat2[led*3+5] = max(int(95*led1_val), dat2[led*3+5])

						if (position < cnt/2): # Since I have no idea what I'm doing, we have to make sure this doesn't wrap around ahead of our shooting star.
							dat2[led*3] = min(int(100*led2_val), dat2[led*3])
							dat2[led*3+1] = min(int(105*led2_val), dat2[led*3+1])
							dat2[led*3+2] = min(int(95*led2_val), dat2[led*3+2])
				except IndexError:
					pass

		if loop:
			data = collections.deque(dat1 + dat2)
			data.rotate(rotate*3)
		else:
			data = dat1


		stk.set_led_data(0, data) # Send off to the blinkstick
		time.sleep(0.02) # Nap for a bit so we don't overwhelm the blinkstick.

		counter = counter + 1

		if counter % freq == 0 and random.randint(1,odds) == 1:
			stars = stars + [ShootingStar()]
			print('star added')


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
	signal(SIGINT, handler)

	print("It's lit bruv. Press CTRL-C to turn down.")
	while True:
		main()
