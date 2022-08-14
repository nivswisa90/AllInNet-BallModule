import sys

from ballmodule.ball_detection.detection import Detection
from ballmodule.utils.utils import send_results, send_frames, delete_frames


def main():
    if len(sys.argv) > 1:
        token = sys.argv[1]
        training_program_id = sys.argv[2]
        min_request_positions = sys.argv[3][0:len(sys.argv[3])].split(',')
        title = ''
        for i in range(4, len(sys.argv)):
            title += sys.argv[i] + ' '
        title = title[:-1]
    else:
        raise Exception("Not enough arguments specified")
    ballModule = Detection(training_program_id, min_request_positions, title)
    payload = ballModule.get_payload()
    try:
        ballModule.open_video()
        ballModule.set_new_throw()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        send_results(payload, token)
        send_frames(training_program_id, token)
        delete_frames()


if __name__ == "__main__":
    main()
