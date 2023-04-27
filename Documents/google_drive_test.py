#Followed tutorial from https://www.youtube.com/watch?v=JwGzHitUVcU
#To generate Tokens: https://developers.google.com/oauthplayground/?code=4/0AVHEtk73eWOZvkVXY1H_fDGe-vpiEHhqh1vZSYUH7ZDQTaaK7nrvGbyTlOErsGYmQbxPnA&scope=https://www.googleapis.com/auth/drive
import json
import requests

header = {"authorization": "Bearer ya29.a0Ael9sCPYkRntofUdhLflHEx-iBJDNgvBZVrBpC3RBR1kbHbigzhyOvm_Rx129vVZJYRTXim9aZ5FmJ4MIjx7beapdO9Qqgta5ktoUcp58_DCCvkBV0Byim7plw_BGE3GAVNKzWB7PtG_766e98r-hC5rzU3paCgYKAUcSARASFQF4udJh-T_UwxDfgvjl3UcmgDe10w0163"}

param = {"name": "face.jpg",
        "parents": ['1AR3SLYY2wgiHyrXQBzQYqjTzHXERiog_']}

files = {'data': ('metadata', json.dumps(param), 'application/json;charset=UTF-8'),
         'file':('face.jpg', open('face.jpg', 'rb'), 'image/jpeg')}
         
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers = header,
    files = files)
    
if r.status_code == 200:
    print("File uploaded succesfully!")
else:
    print("Failed to upload files :(")
