import qi
import time
import random
from copy import deepcopy

def format_dictionary_from_memory(item):
    dictionary = {}
    for key, val in item:
        if key in ['game_id', 'round', 'progressive_id']: val = int(val)
        dictionary[key] = val
    return dictionary

def game_state_handler(game_state, memory):
    game_info = format_dictionary_from_memory(memory.getData('game_info'))
    if game_state == 'voting_night':
        # TODO: with flask
        player_to_kill = [] #simulate_night_votation(game_info)
        memory.insertData('votes', player_to_kill)
        print(game_info['round'], player_to_kill)
    elif game_state == 'voting_day':
        # TODO: with flask
        votes = [] #simulate_daytime_votation(game_info)
        memory.insertData('votes', votes)
        print(game_info['round'], votes)


def send_data(data):
    # TODO: send data to the web page via flask
    ...

def get_data(data):
    # TODO: get data page via flask
    ...

if __name__ == "__main__":
    # TODO subscription to be fixed
    # simulate()
    
    robot_ip = '127.0.0.1'
    robot_port = 9559
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))

    memory = session.service("ALMemory")
    game_state = memory.getData('game_state')
    print(game_state)
    
    game_state_handler(game_state, memory)
