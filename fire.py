from blinkstick import blinkstick
from time import sleep, time
from math import sin
from colorsys import hsv_to_rgb

from signal import signal, SIGINT
from sys import exit
####
# fire.py by Different55 <burritosaur@protonmail.com>
# This script glows red and orange and flickers like a fire.
####


#To exit gracefully on CTRL-C
def turn_off(_, __):
    sticks = blinkstick.find_all()
    for stick in sticks:
        stick.set_led_data(0, [0, 0, 0]*stick.get_led_count())

    print("\nLater skater :)")
    exit(0)



########## -------- MAIN FUNCTION ------- #########
def main():
    ### START OPTIONS ###
    speed = 2 # Overall speed of the animation
    popspeed = 4 # Speed of the flickers/pops
    ### END OPTIONS ###

    #try to find the blinkstick
    try:
        stk = blinkstick.find_first()
        cnt = stk.get_led_count()
        print("It's lit bruv. Press CTRL-C to turn down.")
    #exit if not found
    except:
        print("Blinkstick not detected. Is it plugged in?")
        exit(0)

    #### START MAIN LOOP ####
    errors = 0
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

        #try to write the colors to the strip
        try:
            stk.set_led_data(0, data)
        #if there's an error, increment the error counter and try again
        except:
            errors += 1
            #if we accumulate more than 10 errors without a successful write,
            #strip is probably unplugged, so exit program
            if errors > 15:
                print("Looks like we've been unplugged!")
                exit(0)
        #else if write successful, reset the error counter
        else:
            errors = 0

        sleep(0.02) # Nap for a bit so we don't overwhelm the blinkstick.
    #### END MAIN LOOP ####



if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, turn_off)

    main()
