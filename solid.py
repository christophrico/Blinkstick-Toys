from blinkstick import blinkstick

####
# solid.py by Different55 <burritosaur@protonmail.com>
# This script sets all LEDs on the first blinkstick found to a single solid
# color. You can change the color by modifying the code below.
####

stk = blinkstick.find_first()
cnt = stk.get_led_count()

stk.set_led_data(
    0, [0, 50, 0] * cnt
)  # change the color here. Remember, the format is GRB.
