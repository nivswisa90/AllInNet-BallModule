import pathlib
import cv2
import cvzone
from ballmodule import config
from ballmodule.utils.utils import find_colors, frames_path
import time


class Detection:
    def __init__(self, training_program_id, min_request_positions):
        self.current_position = 0

        self.payload = {
            "id": training_program_id,
            "counterThrowPos1": 0,
            "successfulThrowPos1": 0,
            "counterThrowPos2": 0,
            "successfulThrowPos2": 0,
            "counterThrowPos3": 0,
            "successfulThrowPos3": 0,
            "counterThrowPos4": 0,
            "successfulThrowPos4": 0,
            "counterThrowPos5": 0,
            "successfulThrowPos5": 0,
            "counterThrowPos6": 0,
            "successfulThrowPos6": 0,
            'totalThrows': 0,
            "min1": int(min_request_positions[0]),
            "min2": int(min_request_positions[1]),
            "min3": int(min_request_positions[2]),
            "min4": int(min_request_positions[3]),
            "min5": int(min_request_positions[4]),
            "min6": int(min_request_positions[5]),
        }

        # Video
        self.video_name = pathlib.Path(__file__).parent.parent.parent / config['video']

        limits = config['imgLimits']
        self.min_limit_y, self.max_limit_y, self.min_limit_x, self.max_limit_x, self.minimal_x = limits['minY'], \
                                                                                                 limits['maxY'], \
                                                                                                 limits['minX'], \
                                                                                                 limits['maxX'], \
                                                                                                 limits['maxX']

        # Bbox
        self.bbox = config['bbox']
        self.x_left, self.y_left, self.x_right, self.y_right = self.bbox["xLeft"], self.bbox["yLeft"], \
                                                               self.bbox["xRight"], self.bbox["yRight"]
        self.hsv_val = config['hsvValues']

        # Hoop
        hoop = config['hoop']
        self.x_hoop, self.y_hoop = hoop["x"], hoop["y"]

        # minimal area for color detection
        self.min_area = config['minimal_area']

        # Variables
        self.count_min_x = 0
        self.is_throw = 0
        self.possible_success = 0
        self.pos_list_x = []
        self.pos_list_y = []
        self.ball_bbox_positions = []
        self.was_successful = 0

    def detect_throws(self, img, frame):
        # Initialization of the frame
        img_color, mask = find_colors(img, self.hsv_val)
        img_contours, contours = cvzone.findContours(img, mask, minArea=self.min_area)

        # Ball detected
        if contours:
            ball_x, ball_y = contours[0]['center']
            self.pos_list_x.append(ball_x)
            self.pos_list_y.append(ball_y)

            # Condition to check if it is a new throw
            if len(self.pos_list_x) > 1:
                half_frame_x = self.max_limit_x / 2

                # self.posListX[-2] is the last point of the path of last throw,
                # self.posListX[-1] is the first point of the path of the new throw
                if self.pos_list_x[-2] <= half_frame_x <= self.pos_list_x[-1]:
                    self.set_new_throw()

            # If the ball is above the high of the hoop
            if ball_y < self.y_hoop:
                self.check_throw(ball_x)
                # If the ball passed above the hoop it has a possibility to success
                if self.x_left + 10 <= ball_x <= self.x_right + 10 and self.y_left - 50 <= ball_y <= self.y_right - 50:
                    self.possible_success = 1
            # The ball is bellow the high of the hoop
            else:
                # The ball is bellow the imaginary successful rectangle bellow the hoop
                # No possible success throw, and the throw is close to finish or is done
                if ball_y >= self.y_right:
                    self.is_throw = 0
                    self.possible_success = 0
                # Verify that the ball passes through the imaginary rectangle above the hoop
                if self.x_left <= ball_x <= self.x_right and self.y_left <= ball_y <= self.y_right \
                        and self.is_throw == 1 and self.possible_success == 1:
                    self.ball_bbox_positions.append((ball_x, ball_y))
                # Throw is released, re-initializing all variables.
                self.minimal_x = self.max_limit_x
                self.count_min_x = 0
                # Position list holds at least 2 positions inside the imaginary rectangle bellow the hoop
                if len(self.ball_bbox_positions) > 1:
                    self.write_throw_and_clean()

        self.print_dots(frame)

        if len(self.pos_list_x):
            if self.pos_list_y[-1] >= self.y_right or self.pos_list_x[-1] <= self.x_hoop:
                self.save_throw(frame)
        return img_contours

    def set_throw_position(self):
        y_position = self.pos_list_y[0]
        if 15 <= y_position <= 75:
            self.increment_throw_position(2)
        elif 75 < y_position <= 140:
            self.increment_throw_position(3)
        elif 140 < y_position <= 250:
            self.increment_throw_position(4)

    def print_dots(self, img_contours):
        if self.was_successful == 1:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        for (posX, posY) in (zip(self.pos_list_x, self.pos_list_y)):
            cv2.circle(img_contours, (posX + self.min_limit_x, posY + self.min_limit_y), 5, color, cv2.FILLED)

    def write_throw_and_clean(self):
        self.was_successful = 1
        self.possible_success = 0
        self.is_throw = 0
        self.increment_success_position()
        self.ball_bbox_positions = []

    def get_hsv_val(self):
        return self.hsv_val

    def get_video_parameters(self):
        return self.video_name, self.min_limit_y, self.max_limit_y, self.min_limit_x, self.max_limit_x

    def save_throw(self, img_contours):
        throw_counter = self.payload['totalThrows']
        # frames_path = 'Frames'
        current_frame = f'{frames_path}/frame{throw_counter}.jpg'
        if throw_counter > 0:
            cv2.imwrite(current_frame, img_contours)

    def open_video(self):
        # for video in self.videoName:
        cap = cv2.VideoCapture(f'{self.video_name}')

        while True:
            success, img = cap.read()
            if success:
                # Frame is the entire image and image is the hook zone in the frame
                frame = img
                img = img[self.min_limit_y:self.max_limit_y, self.min_limit_x:self.max_limit_x]
                imageContours = self.detect_throws(img, frame)
                cv2.imshow("ImageColor", frame)
                cv2.waitKey(1)
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    def increment_success_position(self):
        success_position = self.current_position
        if success_position == 2:
            self.payload['successfulThrowPos2'] += 1
        elif success_position == 3:
            self.payload['successfulThrowPos3'] += 1
        elif success_position == 4:
            self.payload['successfulThrowPos4'] += 1

    def increment_throw_position(self, position):
        self.current_position = position
        if position == 2:
            self.payload['counterThrowPos2'] += 1
        elif position == 3:
            self.payload['counterThrowPos3'] += 1
        elif position == 4:
            self.payload['counterThrowPos4'] += 1
        self.payload['totalThrows'] += 1

    def get_payload(self):
        return self.payload

    def set_new_throw(self):
        new_throw_first_point = (self.pos_list_x[-1], self.pos_list_y[-1])
        self.was_successful = 0
        # Clean positions of last throw
        self.pos_list_x = []
        self.pos_list_y = []

        # Append first position of the new throw
        self.pos_list_x.append(new_throw_first_point[0])
        self.pos_list_y.append(new_throw_first_point[1])

        # New throw is starting
        self.possible_success = 0
        self.is_throw = 0
        self.minimal_x = self.max_limit_x
        self.count_min_x = 0

    def check_throw(self, ball_x):
        if ball_x < self.minimal_x:
            self.minimal_x = ball_x
            self.count_min_x += 1
            # 3 Steps is enough to say THROW !
            if self.count_min_x == 3:
                self.is_throw = 1
                self.set_throw_position()
