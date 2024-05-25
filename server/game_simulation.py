from copy import deepcopy
import time
import random
import qi


def format_dictionary_from_memory(item):
    dictionary = {}
    for key, val in item:
        if key in ['game_id', 'round', 'progressive_id']: val = int(val)
        dictionary[key] = val
    return dictionary



#TODO TAKE INSTEAD FROM SOCKET
def get_night_votation():
    # id of players that want killer
    return ...# player_to_kill


    

def simulate_night_votation(game_info):
    killable_players = []
    for i in range( len(game_info['players']) ):
        if game_info['roles'][i] != 'wolf' and game_info['alive'][i]:
            killable_players.append( game_info['players'][i] )
    player_to_kill = game_info['players'].index(random.choice(killable_players)) 
    return player_to_kill

#TODO TAKE INSTEAD FROM SOCKET
def get_daytime_votation():
    # list [g1_votes, ...., gk_votes ]
    return ... # players_votes


def simulate_daytime_votation(game_info):
    players_votes = [0] * len(game_info['players'])
    for _ in range( game_info['alive'].count(True) ):
        players_votes[ random.randint(0, len(players_votes) - 1) ] += 1
    return players_votes


def game_state_handler(game_state, memory):
    game_info = format_dictionary_from_memory(memory.getData('game_info'))
    if game_state == 'voting_night':
        player_to_kill = simulate_night_votation(game_info)
        memory.insertData('votes', player_to_kill)
        print(game_info['round'], player_to_kill)
    elif game_state == 'voting_day':
        votes = simulate_daytime_votation(game_info)
        memory.insertData('votes', votes)
        print(game_info['round'], votes)


def simulate():
    robot_ip = '127.0.0.1'
    robot_port = 9559
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))

    memory = session.service("ALMemory")
    
    try: memory.getData('game_state')
    except: memory.insertData('game_state', "starting")
    
    # TODO fix subscription (for the moment it's not reactive)
    subscriber_game_state = memory.subscriber('game_state')
    connection_game_state = subscriber_game_state.signal.connect(lambda game_state: game_state_handler(game_state, memory))
    
    while memory.getData('game_state') != 'end': 
        print(memory.getData('game_state'))
        time.sleep(0.5)
    
    subscriber_game_state.signal.disconnect(connection_game_state)


if __name__ == "__main__":
    # TODO subscription to be fixed
    # simulate()
    
    robot_ip = '127.0.0.1' #'127.0.0.1'
    robot_port = 9559
    # app = qi.Application(["game_simulation", "--qi-url=tcp://{}:{}".format(robot_ip, robot_port)])
    # app.start()
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))

    print(session)

    memory = session.service("ALMemory")
    # game_state = memory.getData('game_state')
    # print(game_state)
    
    # game_state_handler(game_state, memory)