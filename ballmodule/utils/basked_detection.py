import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

# cap = cv2.VideoCapture("../../Videos/training3-sides.h264")

# Color finder object, False no debug mode
myColorFinder = ColorFinder(True)
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 28, 'smax': 122, 'vmax': 79}

# Variables
# posListX = []
# posListY = []
# posList = []
#
# listX = [item for item in range(0, 1300)]
# start = True


while True:
    # Grab the image
    # success, img = cap.read()
    img = cv2.imread("../../Videos/test.png")
    # The first part is the high, the second the width
    # imgRed, _ = myColorFinder.update(img, "red")
    # imgGreen, _ = myColorFinder.update(img, "green")
    # imgBlue, _ = myColorFinder.update(img, "blue")
    # imgOrange, _ = myColorFinder.update(img, hsvVals)
    # img = img[100:350, 0:350]

    # Find the color ball
    imgColor, mask = myColorFinder.update(img, hsvVals)

    # Find location of the ball
    imgContours, contours = cvzone.findContours(img, mask, minArea=45)

    if contours:
        # contours[0] is the biggest
        cx, cy = contours[0]['center']
        if cx < 1300:
            print(cx, cy)
            cv2.circle(imgContours, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    # for pos in posList:
    #     cv2.circle(imgContours, pos, 5, (0, 255, 0), cv2.FILLED)

    # Display the Video
    # The last two values are the size of the Video
    imgColor = cv2.resize(imgColor, (0, 0), None, 0.9, 0.9)
    # cv2.imshow("Image", img)
    cv2.imshow("ImageColor", imgColor)
    # Video velocity
    cv2.waitKey(90)
