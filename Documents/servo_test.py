import time
from gpiozero import Buzzer
buzzer = Buzzer(12)
buzzer.on()
time.sleep(1)
buzzer.off()

