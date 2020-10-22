from blinkstick import blinkstick
import time, colorsys
from math import sin

from signal import signal, SIGINT
from sys import exit
####
# fireflies.py by Different55 <burritosaur@protonmail.com>
# It lights up random LEDs in a way that looks similar to fireflies at night.
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
    speed = 1 # Overall speed of the animation.
    ff_speed = 5 # Speed of the fireflies.
    fps = 50.0 # FPS of the animation. 50 is about the upper limit.
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
    errors=0
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

        time.sleep(1/fps) # Nap for a bit so we don't overwhelm the blinkstick.
    #### END MAIN LOOP ####


if __name__ == '__main__':
    # Tell Python to run the turn_off() function when SIGINT is recieved
    signal(SIGINT, turn_off)

    main()
