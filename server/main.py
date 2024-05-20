import qi
from server import initialize_game, game
from utils import load_data_from_json, save_data_to_json

def main():
    robot_ip = '127.0.0.1'
    robot_port = 9559
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))

    tts = session.service("ALTextToSpeech")
    memory = session.service("ALMemory")
    dialog = session.service("ALDialog")
    dialog.setLanguage('English')
    logger = qi.logging.Logger("game")

    # database_filename = "database.json" 
    database_filename = "/home/robot/playground/pepper-narrator/server/database.json" # from docker playground (note: python 2.7)
    memory.insertData("database_filename", database_filename)
    
    database = load_data_from_json("/home/robot/playground/pepper-narrator/server/database.json")
    memory.insertData("state", "initialization")
    game_info, alive_wolves, alive_no_wolves = initialize_game(tts, memory, dialog, database, logger)
    
    cache_filename = "game_{}_cache.json".format(database['progressive_id'])
    game(game_info, alive_wolves, alive_no_wolves, cache_filename)
    
    save_data_to_json(database_filename, database)
    
    
    
if __name__ == "__main__":
    main()
