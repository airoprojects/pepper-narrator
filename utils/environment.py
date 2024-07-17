import os
import qi
import sys
import time
import random
import argparse
from copy import deepcopy


# add project root to sys path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)


#
parser = argparse.ArgumentParser()
parser.add_argument('-p','--port', type=str, help="Insert pepper port")
args = parser.parse_args()

robot_ip = '127.0.0.1'
robot_port = int(args.port) if args.port else 9559  
session = qi.Session()
session.connect("tcp://{}:{}".format(robot_ip, robot_port))

# al-memory setup
tts = session.service("ALTextToSpeech")
tts.setParameter("speed", 400)
memory = session.service("ALMemory")
logger = qi.logging.Logger("game")

print('v:(sopra riga 34)',  memory.getData('violence')) # reset the memory
# insert enviroment situation in pepper
memory.insertData('violence', 'false')
memory.insertData('opened_eyes', 'false')

while(True):
    event = raw_input('Trigger event:')
    if(event == 'violence'): memory.insertData('violence', 'true')
    if(event == 'time'): 
        late_players = raw_input('late players: ')
        memory.insertData('time', 'true')
        memory.insertData('late_players', late_players)
        print(late_players)
    if(event == 'joke'): 
        # late_players = raw_input('tease players: ')
        memory.insertData('joke', 'true')
        # memory.insertData('late_players', late_players)
        # print(late_players)
    if(event == 'opened_eyes'): 
        
        memory.insertData('opened_eyes', 'true')


        



 
# TODO:
# """

#     Medium:
#     1. prendere per il culo quello che e' stato votato piu spesso

#     Hard:
#     1. un giocatore apre gli occhi
#     2. un utente che colpisce una categoria particolare di persone
#     3. un utente se ne va

# """