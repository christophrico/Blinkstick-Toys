from blinkstick import blinkstick

stk = blinkstick.find_first()

cnt = stk.get_led_count()

stk.set_led_data(0, [0, 50, 0] * cnt) # change the color here. Remember, the format is GRB.