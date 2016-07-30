from blinkstick import blinkstick
import time, math, colorsys

####
# sky.py by Different55 <burritosaur@protonmail.com>
# This script is made to look like a clear (or not so clear) sky during the day.
# It can draw a clear, sunny sky or a cloudy, overcast sky.
####

fps = 50.0 # FPS of the animation. 50 is about the upper limit.
loop = True # Whether or not to put a sun on both ends of the attached LEDs.
sunny = True # If true, draw and display the sun.
cloudy = False # If true, cut saturation to make it look overcast.

sun1 = [0.11, .9, 1] # These are in hsv format
sun2 = [0.14, .98, 1] # Color of the sun
sky1 = [0.6, .7, .7] # Color of the sky 
sky2 = [0.45, .8, .65] # It'll shift between the two colors.

size1 = 3 # Size of the sun in LEDs
size2 = 4 # The size changes and creates a glowing, pulsing effect.
sun_speed = 5 # Speed of the sun animation
sky_speed = 1 # Speed of the sky animation

### END OPTIONS ###

stk = blinkstick.find_first()
cnt = stk.get_led_count()

if cloudy: # If it's cloudy, cut the saturation.
	sun1[1] = (sun1[1]+.1)/2
	sun2[1] = (sun2[1]+.1)/2
	sky1[1] = (sky1[1]+.3)/3
	sky2[1] = (sky2[1]+.3)/3

while True:
	data = []
	for i in range(cnt):
		sky_color = (math.sin((time.time())*sky_speed+i)/2+.5)
		sun_color = (math.sin((time.time())*sun_speed+i*sun_speed*1.5)/2+.5)
		
		size = size1+(size2-size1)*sun_color
		
		if loop:
			sun_factor = min(max(size-i, 0) + max(size-(cnt-i), 0), 1)
		else:
			sun_factor = min(max(size-i, 0), 1)
		
		sky_hue = sky1[0]+(sky2[0]-sky1[0])*sky_color
		sky_sat = sky1[1]+(sky2[1]-sky1[1])*sky_color
		sky_val = sky1[2]+(sky2[2]-sky1[2])*sky_color
		
		
		hue = sky_hue
		sat = sky_sat
		val = sky_val
		
		r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
		
		if sun_factor > 0 and sunny:
			sun_hue = sun1[0]+(sun2[0]-sun1[0])*sun_color
			sun_sat = sun1[1]+(sun2[1]-sun1[1])*sun_color
			sun_val = sun1[2]+(sun2[2]-sun1[2])*sun_color
			
			sr, sg, sb = colorsys.hsv_to_rgb(sun_hue, sun_sat, sun_val)
			
			r = r+(sr-r)*sun_factor
			g = g+(sg-g)*sun_factor
			b = b+(sb-b)*sun_factor
			
		data = data + [int(g*255), int(r*255), int(b*255)] # Convert to GRB and add to the frame.
	stk.set_led_data(0, data) # Send off to the blinkstick
	time.sleep(1/fps) # Nap for a bit so we don't overwhelm the blinkstick.
