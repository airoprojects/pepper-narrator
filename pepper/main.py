import sys
import time
import random
import qi

sys.path.append("../server")
from server import game

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
    game_info = initialize_game(tts, memory, dialog, database, logger)
    alive_wolves = [ game_info["roles"][i] == "wolf" and game_info["alive"][i] for i in range(len(game_info["players"])) ].count(True)
    alive_no_wolves = [ game_info["roles"][i] != "wolf" and game_info["alive"][i] for i in range(len(game_info["players"])) ].count(True)
    print(game_info, alive_wolves, alive_no_wolves)
    
    # cache_filename = "game_{}_cache.json".format(database['progressive_id'])
    # game(game_info, alive_wolves, alive_no_wolves, cache_filename)
    
    save_data_to_json(database_filename, database)
    
    return 0
    
    
if __name__ == "__main__":
    main()
