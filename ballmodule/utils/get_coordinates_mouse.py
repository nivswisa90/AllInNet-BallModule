# importing the module
import json
import pathlib

import cv2
# from ballmodule import config
# from ballmodule.utils.utils import open_configuration_to_write

# video_name = pathlib.Path(__file__).parent.parent.parent / config['video']


# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        with open("../configs/config.json") as config_file:
            config_object = json.load(config_file)
        config_object['hoop']['x'] = x - config_object['imgLimits']['minX']
        config_object['hoop']['y'] = y - config_object['imgLimits']['minY']
        with open("../configs/config.json", 'w') as config_file:
            json.dump(config_object, config_file)
        # open_configuration_to_write(config)


# driver function
if __name__ == "__main__":
    # reading the image
    # cap = cv2.VideoCapture(f'{video_name}')
    cap = cv2.VideoCapture(0)

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
