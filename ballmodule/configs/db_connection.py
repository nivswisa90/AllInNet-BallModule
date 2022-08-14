import pathlib

import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()


def get_database():
    CONNECTION_STRING = os.getenv('MONGO_URI')
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    all_in_net = client['all_in_net']
    configuration = all_in_net['configuration']

    for item in configuration.find({"title": "CenterLine"}):
        data = {
            'hsvValues': {
                'hmin': item['hsvValues']['hmin'],
                'smin': item['hsvValues']['smin'],
                'vmin': item['hsvValues']['vmin'],
                'hmax': item['hsvValues']['hmax'],
                'smax': item['hsvValues']['smax'],
                'vmax': item['hsvValues']['vmax']
            },
            'video': item['video'],
            'imgLimits': {
                'minX': item['imgLimits']['minX'],
                'maxX': item['imgLimits']['maxX'],
                'minY': item['imgLimits']['minY'],
                'maxY': item['imgLimits']['maxY'],
            },
            'bbox': {
                'xLeft': item['bbox']['xLeft'],
                'xRight': item['bbox']['xRight'],
                'yLeft': item['bbox']['yLeft'],
                'yRight': item['bbox']['yRight']
            },
            'minimal_area': item['minimal_area'],
            'hoop': {
                'x': item['hoop']['x'],
                'y': item['hoop']['y']
            }
        }
        jsonString = json.dumps(data)
        parent = pathlib.Path(__file__).parent.resolve()
        jsonFile = open(parent / "../configs/config.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()