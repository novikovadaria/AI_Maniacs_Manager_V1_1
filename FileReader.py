import os
import json

def find_mp3_file(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            return os.path.join(folder_path, file)
    return None

def read_api_key(file_name='settings.json'):
    with open(file_name, 'r') as file:
        data = json.load(file)
        return data["API_KEY"]
