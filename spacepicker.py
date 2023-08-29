import cv2
import pickle

width, height = 155 - 50, 192 - 143

try:
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseclick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('carParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread('data/carParkImg.png')
    cv2.rectangle(img, (50, 143), (155, 192), (0, 255, 0), 2)

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 0), 2)

    cv2.imshow("Parking Lot", img)
    cv2.setMouseCallback('Parking Lot', mouseclick)
    cv2.waitKey(1)
