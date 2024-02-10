import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://facerecognition-f3cd2-default-rtdb.asia-southeast1.firebasedatabase.app/",
                        'storageBucket':"facerecognition-f3cd2.appspot.com"})

# importing the mode images
folderPath = 'C:\\Users\\praty\\PycharmProjects\\pythonProject1\\images'  # Double backslashes for Windows paths
pathList = os.listdir(folderPath)
imgList = []
studentsID = []
for path in pathList:  # Fixing the variable name here
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentsID.append(os.path.splitext(path)[0])
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentsID)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithID = [encodeListKnown,studentsID]
print("Encoding Complete")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithID,file)
file.close()
print("File closed")


