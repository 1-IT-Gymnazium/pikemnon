import json

SCALE = 0
with open('config.json') as f:
    SCALE = json.load(f)['SCALE']