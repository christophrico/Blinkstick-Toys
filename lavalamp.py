from blinkstick import blinkstick
from time import sleep, time
from colorsys import hsv_to_rgb
from math import sin

from sys import exit
from signal import signal, SIGINT

####
# lavalamp.py by Different55 <burritosaur@protonmail.com>
# This script smoothly and slowly shifts between many colors. It's not actually
# anything like a lavalamp, it just kind of reminded me of one.
####


# To exit gracefully ob CTRL-C
def turn_off(_, __):
    sticks = blinkstick.find_all()
    for stick in sticks:
        stick.set_led_data(0, [0, 0, 0] * stick.get_led_count())

    print("\nLater skater :)")
    exit(0)


########## -------- MAIN FUNCTION ------- #########
def main():
    ### START OPTIONS ###
    fps = 50.0  # FPS of the animation. 50 is about the upper limit.
    speed = 1  # Speed of animation
    type = 1.0  # "1" for hard edges on colors, "1.0" for smooth fading.
    brightness = 1.0  # Brightness of animation, from 0 to 1
    ### END OPTIONS ###

    # try to find the blinkstick
    try:
        stk = blinkstick.find_first()
        cnt = stk.get_led_count()
        print("It's lit bruv. Press CTRL-C to turn down.")
    # exit if not found
    except:
        print("Blinkstick not detected. Is it plugged in?")
        exit(0)

    #### START MAIN LOOP ####
    errors = 0
    while True:
        data = []
        # choose and set the colors
        for i in range(1, cnt + 1):
            (r, g, b) = hsv_to_rgb(
                (sin(time() / (8.0 / speed) + i / (4 * type)) + 1) / 2, 1, brightness
            )
            data = data + [int(g * 255), int(r * 255), int(b * 255)]

        # try to write the colors to the strip
        try:
            stk.set_led_data(0, data)
        # if there's an error, increment the error counter and try again
        except:
            errors += 1
            # if we accumulate more than 10 errors without a successful write,
            # strip is probably unplugged, so exit program
            if errors > 250:
                print("Looks like we've been unplugged!")
                exit(0)

        # else if write successful, reset the error counter
        else:
            errors = 0

        sleep(1 / fps)
    #### END MAIN LOOP ####


if __name__ == "__main__":
    # Tell Python to run the turn_off() function when SIGINT is recieved
    signal(SIGINT, turn_off)

    main()
