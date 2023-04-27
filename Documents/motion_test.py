from gpiozero import MotionSensor
import time

pir = MotionSensor(17)

while True: 
	if pir.motion_detected:
		print("Motion Detected!")
	else:
		print("No motion detected!")
	time.sleep(1)
