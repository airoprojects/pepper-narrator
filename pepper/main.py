import os
import qi
import sys
import time
import random
import argparse
from copy import deepcopy
from functools import partial

import signal
import sys

# add project root to sys path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from utils.utils import load_data_from_json, save_data_to_json, reset_memory
from pepper_functions import *        


global memory


def signal_handler(sig, frame):
    print("Received signal ",  sig, " Cleaning up...")
    reset_memory(memory)
    sys.exit(0)  # Exit the program cleanly


def main():
    
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler) # Handle kill command

    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port', type=str, help="Insert pepper port")
    # parser.add_argument('--reset', action='store_true', help="Reset memory before starting")

    args = parser.parse_args()

    robot_ip = '127.0.0.1'
    robot_port = int(args.port) if args.port else 9559  
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))

    tts = session.service("ALTextToSpeech")
    tts.setParameter("speed", 400)
    memory = session.service("ALMemory")
    logger = qi.logging.Logger("game")
    motion = session.service("ALMotion")
    
    dialog = session.service("ALDialog")
    dialog.setLanguage('English')
    
    # reset memory before start
    reset_memory(memory)
    
    database_filename = "../data/database.json"
    memory.insertData("database_filename", database_filename)
    
    database = load_data_from_json(database_filename)
    memory.insertData("state", "initialization")
    game_info = initialize_game(tts, memory, dialog, database, logger, motion)
    # game_info = deepcopy(database["games"]["1"]) 
    if memory.getData("state") == "end": return None
    
    tts.say("Starting...")
    memory.insertData("state", "game_loop")
    game(game_info, tts, motion, memory, dialog, database, logger)
    # save_data_to_json(database_filename, database)

    return 0 

       
if __name__ == "__main__": 
    main()
