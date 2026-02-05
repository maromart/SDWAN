import json
import os

def savefile(filename,dict):
    try:
        with open(filename, 'w') as jf:
            json.dump(dict, jf, indent=4)
        print(f"File {filename} saved...")
    except Exception as e:
        print(f"File {filename} not saved:", e)


def create_dir(directory):
    try:
        print(f"Creating directory {directory}")
        os.stat(directory)
    except:
        os.mkdir(directory)