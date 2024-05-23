import cv2
import pyglet.media
from cvzone.FaceMeshModule import FaceMeshDetector
import pyfirmata
import csv
from datetime import datetime

import argparse
import time
from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0, help="index of webcam on system")
args = vars(ap.parse_args())

# start the video stream thread
time.sleep(1)
vs = VideoStream(src=args["webcam"]).start()

detector = FaceMeshDetector(maxFaces=1)

breakcount = 0
state = False

sound = pyglet.media.load("alarm.wav", streaming=False)

def recordData(condition):
    file = open("database.csv", "a", newline="")
    now = datetime.now()
    dtString = now.strftime("%d-%m-%Y %H:%M:%S")
    tuple = (dtString, condition)
    writer = csv.writer(file)
    writer.writerow(tuple)
    file.close()

while True:
    frame = vs.read()
    img = cv2.flip(frame, 1)

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        eyeLeft = [27, 23, 130, 243]  # up, down, left, right
        eyeRight = [257, 253, 463, 359]  # up, down, left, right
        mouth = [11, 16, 57, 287]  # up, down, left, right
        faceId = [27, 23, 130, 243, 257, 253, 463, 359, 11, 16, 57, 287]

        #calculate eye left distance ratio
        eyeLeft_ver, _ = detector.findDistance(face[eyeLeft[0]], face[eyeLeft[1]])
        eyeLeft_hor, _ = detector.findDistance(face[eyeLeft[2]], face[eyeLeft[3]])
        eyeLeft_ratio = int((eyeLeft_ver/eyeLeft_hor)*100)
        # calculate eye right distance ratio
        eyeRight_ver, _ = detector.findDistance(face[eyeRight[0]], face[eyeRight[1]])
        eyeRight_hor, _ = detector.findDistance(face[eyeRight[2]], face[eyeRight[3]])
        eyeRight_ratio = int((eyeRight_ver / eyeRight_hor) * 100)
        # calculate mouth distance ratio
        mouth_ver, _ = detector.findDistance(face[mouth[0]], face[mouth[1]])
        mouth_hor, _ = detector.findDistance(face[mouth[2]], face[mouth[3]])
        mouth_ratio = int((mouth_ver / mouth_hor) * 100)

        cv2.imshow("Image", img)#display text on image
        cv2.rectangle(img, (30,20), (400,150), (0,255,255), cv2.FILLED)
        cv2.putText(img, f'Eye Left Ratio: {eyeLeft_ratio}', (50, 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
        cv2.putText(img, f'Eye Right Ratio: {eyeRight_ratio}', (50, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(img, f'Eye Mouth Ratio: {mouth_ratio}', (50, 140),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    
    # rest of your code...



        #drowsiness detection logic
    if (mouth_ratio > 60) or (eyeLeft_ratio <= 50 and eyeRight_ratio <= 50):
            breakcount += 1
            if breakcount >= 30:
                if state == False:
                    sound.play()
                    recordData("Sleep")
                    state = not state
            print("drowsy")
    else:
            breakcount = 0
            if state:
                state = not state
            print("awake")

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    for id in faceId:
            cv2.circle(img,face[id], 5, (0,0,255), cv2.FILLED)
    cv2.waitKey(1)