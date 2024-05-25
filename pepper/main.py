import sys
import time
import random
from copy import deepcopy
import qi


from utils import load_data_from_json, save_data_to_json
from pepper_functions import *        

def main():
    robot_ip = '127.0.0.1'
    robot_port = 9559
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))

    tts = session.service("ALTextToSpeech")
    tts.setParameter("speed", 400)
    memory = session.service("ALMemory")
    logger = qi.logging.Logger("game")
    
    dialog = session.service("ALDialog")
    dialog.setLanguage('English')
    
    database_filename = "../data/database.json"
    memory.insertData("database_filename", database_filename)
    
    database = load_data_from_json(database_filename)
    memory.insertData("state", "initialization")
    # game_info = initialize_game(tts, memory, dialog, database, logger)
    game_info = deepcopy(database["games"]["1"])
    if memory.getData("state") == "end": return None
    
    tts.say("Starting...")
    memory.insertData("state", "game_loop")
    game(game_info, tts, memory, dialog, database, logger)
    # save_data_to_json(database_filename, database)
    
    return 0
    
    
if __name__ == "__main__":
    main()
