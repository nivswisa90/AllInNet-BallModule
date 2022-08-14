import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

# cap = cv2.VideoCapture("../../FiveJune/2PointsTraining.h264")

# Color finder object, False no debug mode
myColorFinder = ColorFinder(True)
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 28, 'smax': 122, 'vmax': 79}


while True:
    # Grab the image
    img = cv2.imread("../../FiveJune/test.png")
    # The first part is the high, the second the width
    img = img[200:450, 0:350]

    # Find the color ball
    imgColor, mask = myColorFinder.update(img, hsvVals)

    # Find location of the ball
    imgContours, contours = cvzone.findContours(img, mask, minArea=45)

    if contours:
        # contours[0] is the biggest
        cx, cy = contours[0]['center']
        if cx < 1300:
            cv2.circle(imgContours, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    # Display the Video
    # The last two values are the size of the Video
    imgColor = cv2.resize(imgColor, (0, 0), None, 0.9, 0.9)

    cv2.imshow("ImageColor", imgColor)
    # Video velocity
    cv2.waitKey(50)
