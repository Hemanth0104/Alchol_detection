# For Dlib
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import pyglet
import argparse
import imutils
import time
import dlib
import cv2
from playsound import playsound
# For cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import pyfirmata
# For YOLO
from ultralytics import YOLO


def sound_alarm(path):
    # play an alarm sound
    music = pyglet.resource.media('alarm.wav')
    music.play()
    pyglet.app.run()

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizon
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

def dlib_detect(frame):
    EYE_AR_THRESH = 0.3

    # grab the indexes of the facial landmarks for the left and right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        #cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:
            return "drowsy",frame
        else:
            return "awake",frame
    return "awake",frame


def yolo_detect(frame):
    results = model.predict(frame)
    result = results[0]
    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        if(class_id=="drowsy"):
            return "drowsy"
        else:
            return "awake"


def cvzone_detect(frame):
    img = cv2.flip(frame, 1)
    img, faces = detector1.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        eyeLeft = [27, 23, 130, 243]  # up, down, left, right
        eyeRight = [257, 253, 463, 359]  # up, down, left, right
        mouth = [11, 16, 57, 287]  # up, down, left, right

        #calculate eye left distance ratio
        eyeLeft_ver, _ = detector1.findDistance(face[eyeLeft[0]], face[eyeLeft[1]])
        eyeLeft_hor, _ = detector1.findDistance(face[eyeLeft[2]], face[eyeLeft[3]])
        eyeLeft_ratio = int((eyeLeft_ver/eyeLeft_hor)*100)
        # calculate eye right distance ratio
        eyeRight_ver, _ = detector1.findDistance(face[eyeRight[0]], face[eyeRight[1]])
        eyeRight_hor, _ = detector1.findDistance(face[eyeRight[2]], face[eyeRight[3]])
        eyeRight_ratio = int((eyeRight_ver / eyeRight_hor) * 100)
        # calculate mouth distance ratio
        mouth_ver, _ = detector1.findDistance(face[mouth[0]], face[mouth[1]])
        mouth_hor, _ = detector1.findDistance(face[mouth[2]], face[mouth[3]])
        mouth_ratio = int((mouth_ver / mouth_hor) * 100)

        # drowsiness detection logic
        if (mouth_ratio > 60) or (eyeLeft_ratio <= 50) or (eyeRight_ratio <= 50):
            return "drowsy"
        else:
            return "awake"
    else:
        return "awake"


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("68_face_landmarks.dat")

model = YOLO("best.pt")

detector1 = FaceMeshDetector(maxFaces=1)

EYE_AR_CONSEC_FRAMES = 15
ALARM_ON = False
COUNTER = 0
output=["temp","temp","temp"]

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0, help="index of webcam on system")
args = vars(ap.parse_args())
# start the video stream thread
time.sleep(1)
vs = VideoStream(src=args["webcam"]).start()

# loop over frames from the video stream
while True:
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    frame = vs.read()
    output[0],frame = dlib_detect(frame)
    output[1] = yolo_detect(frame)
    output[2] = cvzone_detect(frame)
    majority_element = max(output, key=output.count)
    print(output," -> ",majority_element)

    ########## Aakash
    if(majority_element=="drowsy"):
        # if the eyes were closed for a sufficient number of
        # then sound the alarm
        COUNTER = COUNTER + 1
        if COUNTER >= EYE_AR_CONSEC_FRAMES:
            # if the alarm is not on, turn it on
            if not ALARM_ON:
                ALARM_ON = True
            # draw an alarm on the frame
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            playsound('alarm.wav')

    # otherwise, the eye aspect ratio is not below the blink
    # threshold, so reset the counter and alarm
    else:
        COUNTER = 0
        ALARM_ON = False


    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
