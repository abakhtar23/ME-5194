import time
import digitalio
import board
import adafruit_matrixkeypad
from gpiozero import RGBLED
from guizero import App, Slider
from colorzero import Color

rgb_led = RGBLED(18, 23, 24)

red = 0
green = 0
blue=0

# Membrane 3x4 matrix keypad on Raspberry Pi -
# https://www.adafruit.com/product/419
cols = [digitalio.DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
rows = [digitalio.DigitalInOut(x) for x in (board.D5, board.D6, board.D13, board.D19)]

# 3x4 matrix keypad on Raspberry Pi -
# rows and columns are mixed up for https://www.adafruit.com/product/3845
# cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D5, board.D26)]
# rows = [digitalio.DigitalInOut(x) for x in (board.D6, board.D21, board.D20, board.D19)]
pin_base=[1, 2, 3, 4]
keys = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ("*", 0, "#"))
rgb_led.color = Color(255, 0, 0)
def pin_check(pin,guess):
    #print("Code: {}\tGuess: {}".format(code, guess))
    if pin == guess:
        print('Come In')
        rgb_led.color = Color(0, 255, 0 )
        return True
    else:
        print('No')
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
 
    # return string
    return str1
def pin_gen(pin,guess):
    #print("Code: {}\tGuess: {}".format(code, guess))
    if pin == guess:
        print('Door Is Open')
        rgb_led.color = Color(0, 0,255)
        return True
    else:
        print('No')
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
pin_guess=[]
while True:
    if keypad.pressed_keys:
        pin_guess.append((keypad.pressed_keys)[0])
        #z=listToString(code_guess)
        #print(z)
        print(pin_guess)
        time.sleep(0.2)
        if len(pin_guess)>3:
            pin_check(pin_base,pin_guess)
            pin_guess=[]


