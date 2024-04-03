import json
import os
import logging

__author__ = "Mario Uriel Romero Martinez"
__version__ = "1.0"
__maintainer__ = "Mario Uriel Romero Martinez"

def savefile(filename,dict):
    try:
        with open(filename, 'w') as jf:
            json.dump(dict, jf, indent=4)
        print(f"File {filename} saved...")
        logging.info("File %s was saved", filename)
    except Exception as e:
        logging.error("File %s was not saved", filename)
        print(f"File {filename} not saved:", e)


def create_dir(directory):
    try:
        print(f"Creating directory {directory}")
        logging.info("directory %s was created",directory)
        #os.stat(directory)
        os.mkdir(directory)
    except:
        logging.error("Error trying to create the directory")
        os.stat(directory)
        #os.mkdir(directory)