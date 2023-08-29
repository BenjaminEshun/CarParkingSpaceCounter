import cv2
import cvzone
import numpy as np
import pickle

vid_capture = cv2.VideoCapture('data/carPark.mp4')

width, height = 155 - 50, 192 - 143

with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)


def checkParkingSpace(vidProcessing):
    emptySpace = 0

    for pos in posList:
        x, y = pos

        # Cropping parking space
        vidCrop = vidProcessing[y:y + height, x:x + width]


        pixelCount = cv2.countNonZero(vidCrop)
        cvzone.putTextRect(vid, str(pixelCount), (x, y + height - 2), scale=1, thickness=2, offset=0, colorR=(0, 0, 0))

        if pixelCount < 600:
            color = (0, 255, 0)
            thickness = 3
            emptySpace += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(vid, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(vid, f"Empty Spaces: {emptySpace}/{len(posList)}", (350, 50), scale=2, thickness=3, offset=20, colorR=(0, 0, 0))


while True:
    # Loop video
    if vid_capture.get(cv2.CAP_PROP_POS_FRAMES) == vid_capture.get(cv2.CAP_PROP_FRAME_COUNT):
        vid_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, vid = vid_capture.read()

    vidGray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    vidBlur = cv2.GaussianBlur(vidGray, (3, 3), 1)
    vidThreshold = cv2.adaptiveThreshold(vidBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    vidMedian = cv2.medianBlur(vidThreshold, 5)

    kernel = np.zeros((3, 3), np.uint8)
    vidDilate = cv2.dilate(vidMedian, kernel, iterations=1)

    checkParkingSpace(vidDilate)

    cv2.imshow('Car Parking Space Counter', vid)

    cv2.waitKey(20)
