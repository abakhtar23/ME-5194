from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
import threading
import time
import string
import secrets
from fastapi import Request

"""Simple test for 16x2 character lcd connected to an MCP23008 I2C LCD backpack."""
import board
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
# Function to generate a new code every 60 seconds
def generate_code():
    global code
    while True:
    
        alphabet = string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(4))
        time.sleep(60)

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
    
# HTML response with a form that includes a text box for user input
@app.get("/", response_class=HTMLResponse)
async def get_code():
    return """
        <h1>Current Code: {code}</h1>
        <form method="post" action="/">
            <input type="text" name="user_text">
            <input type="submit" value="Submit">
        </form>
    """.format(code=code)

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


#async def update_code(background_tasks: BackgroundTasks, new_code: str):
    #global code
    #code = new_code
    #return {"message": f"Message Sent: {new_code}"}



