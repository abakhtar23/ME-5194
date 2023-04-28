from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
import threading
import time
import string
import secrets
from fastapi import Request
import digitalio
import board
import adafruit_matrixkeypad
from gpiozero import RGBLED
from guizero import App, Slider
from colorzero import Color
import adafruit_character_lcd.character_lcd_i2c as character_lcd


# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 4

# Initialise I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# Initialise the lcd class
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)


app = FastAPI()
code=None

async def generate_code():  # Modify to be an asynchronous function
    global code
    while True:
        alphabet = string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(4))
        time.sleep(60)

# Start the code generation in a separate task on the event loop
async def start_code_generation():
    await generate_code()

# HTML response with a form that includes a text box for user input
@app.get("/", response_class=HTMLResponse)
async def get_code():
    loop = asyncio.get_event_loop()
    loop.create_task(start_code_generation())  # Start the code generation task
    return """
        <h1>Current Code: {code}</h1>
        <form method="post" action="/">
            <input type="text" name="user_text">
            <input type="submit" value="Submit">
        </form>
    """.format(code=code)

# Start the code generation in a separate thread
t = threading.Thread(target=generate_code)
t.start()
def get_text(a,b):
    lcd.clear()
    user_string=a
    code=b
    # Turn backlight on
    lcd.backlight = True
	#Print a two line message
    lcd.message = user_string
	
    print(user_string)
    


# API endpoint to allow users to update the code
@app.post("/")
async def process_text(request: Request):
    form_data = await request.form()
    user_text = form_data.get("user_text")
    if user_text:
        
        # Do something with user_text, such as passing it to a function for further processing
        result = get_text(user_text,code)        #return {"result": result}
    else:
        raise HTTPException(status_code=400, detail="No text provided")

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
second_pin=False
keys = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ("*", 0, "#"))
rgb_led.color = Color(255, 0, 0)
def pin_check(pin,guess,sec):
    #print("Code: {}\tGuess: {}".format(code, guess))
    if pin == guess:
        print('Come In')
        rgb_led.color = Color(0, 255, 0 )
        sec=True
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
        if (len(pin_guess)>3) & (second_pin == False):
            pin_check(pin_base,pin_guess,second_pin)
            print('false')
            pin_guess=[]
        if (len(pin_guess)>3) & (second_pin == True): 
            pin_check(pin_base,pin_guess,second_pin)
            pin_guess=[]
            print('True')
