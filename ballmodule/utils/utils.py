import json
import os
import pathlib
import glob

import requests
from cvzone import ColorFinder

frames_path = pathlib.Path(__file__).parent.parent.parent / 'Frames'


def open_configuration():
    parent = pathlib.Path(__file__).parent.resolve()
    with open(parent / "../configs/config.json") as config_file:
        config_object = json.load(config_file)
    return config_object


def open_configuration_to_write(new_file):
    parent = pathlib.Path(__file__).parent.resolve()
    with open(parent / "../configs/config.json", 'w') as config_file:
        json.dump(new_file, config_file)


def send_results(payload, token):
    print('payload', payload)
    try:
        res = requests.post('http://allinnet.online/api/training/results', data=payload, headers={
            "x-access-token": token
        })
        print(res.text)
        print('{')
        for key, value in payload.items():
            print(f'\t{key}, {value}')
        print('}')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def send_frames(training_program_id, token):
    try:
        multiple_files = []
        directory = pathlib.Path(__file__).parent.parent.parent / 'Frames'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                file = ('multi-files', (f, open(f, 'rb'), 'image/jpg'))
                multiple_files.append(file)
        res = requests.post('http://allinnet.online:5001/api/training/results/upload', files=multiple_files, headers={
            "x-access-token": token,
            "programId": training_program_id
        })
        print(res.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def find_colors(img, hsv_val):
    # Find the color ball
    # Color finder object, False no debug mode
    myColorFinder = ColorFinder(False)
    imgColor, mask = myColorFinder.update(img, hsv_val)
    return imgColor, mask


def delete_frames():
    files = glob.glob(f'{frames_path}/*.jpg')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))