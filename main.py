import cv2
import pickle
import cvzone
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("venv/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://facerecognition-f3cd2-default-rtdb.asia-southeast1.firebasedatabase.app/",
                        'storageBucket':"facerecognition-f3cd2.appspot.com"})

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,477)
# imgBackground = cv2.imread('resources/background.png')

print("Loding Encoding file")
file = open("venv/EncodeFile.p",'rb')
encodeListKnownWithID = pickle.load(file)
file.close()
encodeListKnown, studentsID = encodeListKnownWithID
print(studentsID)
print("Encoded File Loaded")
id = 0
count = 0
while True:
    success, img = cap.read()
    # imgBackground[0:0 + 477, 0:0 + 640] = img
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print("matches",matches)
        print("faceDis",faceDis)

        matchIndex = np.argmin(faceDis)
        print("Match Index",matchIndex)

        if matches[matchIndex]:
            print("Known person detected")
            print(studentsID[matchIndex])
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = x1,y1,x2-x1,y2-y1
            cvzone.cornerRect(img,bbox,rt=0)
            id = studentsID[matchIndex]
            studentInfo = db.reference(f'Students/{id}').get()
            cv2.putText(img,str (studentInfo['Name']), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 255, 255),1)
            print(studentInfo)


    cv2.imshow("Webcam",img)
    # cv2.imshow("Person Detection",imgBackground)
    cv2.waitKey(1)

