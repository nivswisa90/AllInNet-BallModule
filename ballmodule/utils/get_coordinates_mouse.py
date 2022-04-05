# importing the module
import json
import pathlib

import cv2
from ballmodule import config
from ballmodule.utils.utils import open_configuration_to_write

video_name = pathlib.Path(__file__).parent.parent.parent / config['video']


# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        config['hoop']['x'] = x - config['imgLimits']['minX']
        config['hoop']['y'] = y - config['imgLimits']['minY']
        open_configuration_to_write(config)


# driver function
if __name__ == "__main__":
    # reading the image
    cap = cv2.VideoCapture(f'{video_name}')

    try:
        while True:
            success, img = cap.read()
            if success:
                # displaying the image
                cv2.imshow('image', img)

            # setting mouse handler for the image
            # and calling the click_event() function
            cv2.waitKey(1)
            cv2.setMouseCallback('image', click_event)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        # close the window
        cv2.destroyAllWindows()
