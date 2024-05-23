import cv2
from ultralytics import YOLO
from imutils.video import VideoStream
import argparse
import time

model = YOLO("best.pt")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0, help="index of webcam on system")
args = vars(ap.parse_args())
# start the video stream thread
time.sleep(1)
vs = VideoStream(src=args["webcam"]).start()


while True:
    frame = vs.read()
    results = model.predict(frame)
    result = results[0]
    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        print("Object type:", class_id)

