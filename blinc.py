#!/usr/bin/python3
from blinkstick import blinkstick
import sys
from webcolors import name_to_rgb
from time import time, sleep
from math import cos, pi

from signal import signal, SIGINT
from sys import exit


sticks = blinkstick.find_all()

# Defaults
bright = 1
duration = 1
blink_duration = .02
lerp = 'sine'

def syntax():
	print('Usage:', sys.argv[0], '[options] <color(s)>')
	print('Colors and options can be provided in any order. At least one color is required.')
	print('If multiple colors are provided, a transition option must be included')
	print('')
	print('OPTIONS:')
	print('Transition options:')
	print('	--color				Set strip to single color, only first color will be used if multiple are provided. This is the default.')
	print('	--morph				If multiple colors are provided, morphs strip between colors.')
	print('	--flow				Like morph, but the colors smoothly flow in from one side of the strip to the other.')
	print('	--strobe			Briefly flashes between colors and then off.')
	print('	--flash				Hard switches between colors.')
	print('	--brightness=LEVEL	Sets overall brightness of the LEDs from 0-1.')
	print('')
	print('There are a few animation-specific options that can\'t be used with --color:')
	print('	--loop				Loop endlessly over animation.')
	print('	--duration=TIME		Each color phase lasts for this long.')
	print('	--sduration=TIME	How long an individual strobe flash should last. Used with --strobe.')
	print('')
	print('The morph and flow animations have a few different options:')
	print('	--linear			Flat interpolation. Straight from one color to the other.')
	print('	--sine				Ease in and ease out in a sinusoidal way. This is the default.')
	print('	--rev				Starts slow, accelerates until it reaches target color.')
	print('	--leap				Starts fast and decelerates as it gets closer.')
	print('	--blink				Instant shifts from one color to the next.')
	sys.exit(1)

def process_color(color):
	if color[0] == '#': # Hex code
		if len(color) != 7:
			print('Error: not a valid hex code (',color,'). Should match pattern: #RRGGBB')
			syntax()
		else:
			r = int(color[1:3], 16)
			g = int(color[3:5], 16)
			b = int(color[5:7], 16)
			if max(r,g,b) > 255 or max(r,g,b) < 0:
				print('Error: not a valid hex code (',color,'). Values must be in the range 00-FF')
				syntax()
	elif color[0:4] == 'rgb(':
		if color[-1] != ')' or color.count(',') != 2:
			print('Error: not a valid rgb color (',color,'). Should match pattern: rgb(rrr,ggg,bbb)')
			syntax()
		(r, g, b) = color[4:-1].split(',')
		if max(r,g,b) > 255 or max(r,g,b) < 0:
			print('Error: not a valid rgb color (',color,'). Values must be in the range 0-255')
			syntax()
	else:
		try:
			(r, g, b) = name_to_rgb(color)
		except:
			print('Error: could not parse color (',color,'). Not a valid hex code (#RRGGBB), rgb color (rgb(rrr,ggg,bbb)), or HTML WebColor name.')
			syntax()
	return (g, r, b)

def send(g, r, b):
	for stick in sticks:
		if stick.get_led_count() == -1:
			stick.set_color(0, 0, int(g*bright), int(r*bright), int(b*bright))
		else:
			stick.set_led_data(0, [int(g*bright), int(r*bright), int(b*bright)]*stick.get_led_count())

def push(g, r, b):
	for stick in sticks:
		if stick.get_led_count() == -1:
			stick.set_color(0, 0, int(g*bright), int(r*bright), int(b*bright))
		else:
			data = stick.get_led_data(stick.get_led_count()*3) # Old data
			data = [int(g*bright), int(r*bright), int(b*bright)] + list(data[:-3])
			stick.set_led_data(0, data)

def single_color(color):
	(g, r, b) = process_color(color)
	send(g, r, b)

def morph(colorlist, flow):
	curcolor = list(sticks[0].get_led_data(1))
	while True:
		for color in colorlist:
			targetcolor = process_color(color)
			start = time()
			while time()-start < duration:
				progress = (time()-start)/duration
				if lerp == 'sine':
					progress = 1-(cos(pi*progress)+1)/2
				elif lerp == 'leap':
					progress = -1*(progress-1)**2+1
				elif lerp == 'rev':
					progress = progress**2
				elif lerp == 'blink':
					progress = 0
				(g, r, b) = [a*(1-progress)+b*progress for a, b in zip(curcolor, targetcolor)]
				if flow:
					push(g, r, b)
				else:
					send(g, r, b)
				sleep(.02)
			curcolor = targetcolor
		if not loop:
			break

def blink(colorlist, strobe):
	while True:
		for color in colorlist:
			(g, r, b) = process_color(color)
			start = time()
			send(g, r, b)
			if strobe:
				sleep(max(.02, blink_duration))
				send(0, 0, 0)
			sleep(max(.02, duration))
		if not loop:
			break


def handler(signal_received, frame):
	print("\nLater Skater")
	send(0,0,0)
	exit(0)



########## -------- MAIN FUNCTION ------- #########
def main():

	action = 'color'
	loop = False
	colorlist = []

	if len(sys.argv) < 2:
		syntax()

	for arg in sys.argv:
		if arg == sys.argv[0]:
			continue

		if arg == '--color':
			action = 'color'
		elif arg == '--morph':
			action = 'morph'
		elif arg == '--strobe':
			action = 'strobe'
		elif arg == '--flash':
			action = 'flash'
		elif arg == '--flow':
			action = 'flow'

		elif arg == '--linear':
			lerp = 'linear'
		elif arg == '--sine':
			lerp = 'sine'
		elif arg == '--rev':
			lerp = 'rev'
		elif arg == '--leap':
			lerp = 'leap'
		elif arg == '--blink':
			lerp = 'blink'

		elif arg == '--loop':
			loop = True

		elif arg[0:13] == '--brightness=':
			bright = float(arg[13:])
		elif arg[0:11] == '--duration=':
			duration = float(arg[11:])
		elif arg[0:12] == '--sduration=':
			blink_duration = float(arg[12:])

		elif arg == '--help':
			syntax()
		elif arg == '--version':
			print('Blinc by Different55 (burritosaur@protonmail.com) v0.5')

		else:
			colorlist.append(arg)

	if action == 'morph':
		morph(colorlist, False)

	elif action == 'flow':
		if not loop:
			colorlist = colorlist + colorlist[-1] # Duplicate the last color if we're not looping so it gets a chance to cover the entire strip.
		morph(colorlist, True)

	elif action == 'strobe':
		blink(colorlist, True)

	elif action == 'flash':
		blink(colorlist, False)

	elif action == 'color':
		single_color(colorlist[0])



if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
	signal(SIGINT, handler)

	print("It's lit bruv. Press CTRL-C to turn down.")
	while True:
		main()
