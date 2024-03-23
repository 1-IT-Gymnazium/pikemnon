import json

# Initialize variables
SCALE = 0
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0  # Corrected the typo here

# Open the configuration file and load its contents
with open('config.json') as f:
    config = json.load(f)  # Load the JSON data into a variable once
    SCALE = config['SCALE']
    WINDOW_WIDTH = config['WINDOW_WIDTH']
    WINDOW_HEIGHT = config['WINDOW_HEIGHT']  # Corrected variable name
