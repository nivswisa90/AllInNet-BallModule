import json
import os
import pathlib

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


def send_results(payload):
    try:
        res = requests.post('http://allinnet.online/api/training/results', data=payload)
        # res = requests.post('http://localhost:5001/api/training/results', data=payload)
        print(res.text)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)


def send_frames():
    try:
        multiple_files = []
        directory = pathlib.Path(__file__).parent.parent.parent / 'Frames'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                file = ('multi-files', (f, open(f, 'rb'), 'image/jpg'))
                multiple_files.append(file)
        res = requests.post('http://allinnet.online/api/training/results/upload', files=multiple_files)
        # res = requests.post('http://localhost:5001/api/training/results/upload', files=multiple_files)
        print(res.text)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)


def find_colors(img, hsv_val):
    # Find the color ball
    # Color finder object, False no debug mode
    myColorFinder = ColorFinder(False)
    imgColor, mask = myColorFinder.update(img, hsv_val)
    return imgColor, mask
