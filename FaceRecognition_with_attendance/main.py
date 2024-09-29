import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

def faceRecognition_attendance():
    path = 'imagesAttendance'
    images = []
    classNames = []
    mylist = os.listdir(path)
    for cl in mylist:
        curIMG = cv2.imread(f'{path}/{cl}')
        images.append(curIMG)
        classNames.append(os.path.splitext(cl)[0])
    print("Dataset Encoding....")

    def findEncodings(images):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist


    encodelistKnown = findEncodings(images)
    print("Encoding Complete")

    marked_names = set()
    def markAttendance(name):
        if name not in marked_names:
            with open('Attendance.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.strip().split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtstring = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name}, {dtstring}')
                    marked_names.add(name)



    cap = cv2.VideoCapture(0)

    cap.set(3, 1280)
    cap.set(4, 720)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(imgS)
        encodingsCurrentFrame = face_recognition.face_encodings(imgS, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodingsCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodelistKnown, encodeFace)
            distance = face_recognition.face_distance(encodelistKnown, encodeFace)
            matchIndex = np.argmin(distance)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = (y1*4),(x2*4),(y2*4),(x1*4)
                cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                markAttendance(name)

        present = len(marked_names)
        cv2.putText(img, f'Present:- {present}', (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)



        cv2.imshow("webcam", img)
        cv2.waitKey(1)

with open('Attendance.csv', 'r+') as f:
    f.truncate()
    f.writelines("Name, Time")
faceRecognition_attendance()
