import time
import digitalio
import board
import adafruit_matrixkeypad

# Membrane 3x4 matrix keypad on Raspberry Pi -
# https://www.adafruit.com/product/419
cols = [digitalio.DigitalInOut(board.GPIO26), digitalio.DigitalInOut(board.GPIO20), digitalio.DigitalInOut(board.GPIO21)]
rows = [digitalio.DigitalInOut(board.GPIO5), digitalio.DigitalInOut(board.GPIO6), digitalio.DigitalInOut(board.GPIO13), digitalio.DigitalInOut(board.GPIO19)]

keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
    time.sleep(0.1)
