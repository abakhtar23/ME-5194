import cv2
import numpy as np
import time
from imutils.video import VideoStream
from imutils import resize
from datetime import datetime, timedelta


#Followed tutorial from https://www.youtube.com/watch?v=JwGzHitUVcU
#To generate Tokens: https://developers.google.com/oauthplayground/?code=4/0AVHEtk73eWOZvkVXY1H_fDGe-vpiEHhqh1vZSYUH7ZDQTaaK7nrvGbyTlOErsGYmQbxPnA&scope=https://www.googleapis.com/auth/drive
import json
import requests


diff_threshold = 1000000
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
vs = VideoStream(src=0).start()

header = {"authorization": "Bearer ya29.a0Ael9sCOc8t4KR5i59ElWxqF5CrjXwu4HdFl3CcJzsF-Q-LQfv2jdIgEMNwZDOH4dQpNvYLQwdvs11yd5oDFUFWLvAYMMJwp7-HjtlTgJ9NLlDKOcNqRBc_7D9dAtbP2x7f0rM9ygrD5P1IQdxQJvlHbWV_chaCgYKATkSARASFQF4udJh3EJEXtvqXXgLXe5VpCHsfw0163"}

param = {"name": "face.jpg",
        "parents": ['1AR3SLYY2wgiHyrXQBzQYqjTzHXERiog_']}

files = {'data': ('metadata', json.dumps(param), 'application/json;charset=UTF-8'),
         'file':('face.jpg', open('face.jpg', 'rb'), 'image/jpeg')}
         
face_detected = False
start_face = None
while True:
    old_image = vs.read()
    old_image = cv2.cvtColor(old_image, cv2.COLOR_BGR2GRAY)
    old_image = cv2.blur(old_image, (20, 20))

    new_image = vs.read()
    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    new_image = cv2.blur(new_image, (20, 20))

    diff = cv2.absdiff(old_image, new_image)
    diff_score = np.sum(diff)

    if diff_score > diff_threshold:
        print("Movement detected")

    faces = face_cascade.detectMultiScale(new_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) > 0:
        if (not face_detected) and (start_face is None):
            start_face = datetime.now()
            print("Face detected")
            # Take picture and set face_detected flag to True
            cv2.imwrite("face.jpg", new_image)
            face_detected = True
            r = requests.post(
				"https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
				headers = header,
				files = files)
				
            if r.status_code == 200:
                print("File uploaded succesfully!")
            else:
                print("Failed to upload files :(")
    else:
        if face_detected:
            face_detected = False
            
    if (start_face is not None) and (datetime.now() > start_face + timedelta(minutes=1)):
        print("reset")
        start_face = None

    old_image = new_image
