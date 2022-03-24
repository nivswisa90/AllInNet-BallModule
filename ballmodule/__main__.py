import sys

from ballmodule.ball_detection.detection import Detection
from ballmodule.utils.utils import send_results, send_frames


def main():
    # Minimum request
    if len(sys.argv) > 1:
        min_ball_throws = sys.argv[1]
    else:
        min_ball_throws = 3
        # raise Exception("Not enough arguments specified")
    ballModule = Detection(min_ball_throws)
    payload = ballModule.get_payload()
    try:
        ballModule.open_video()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        send_results(payload)
        send_frames()


if __name__ == "__main__":
    main()
