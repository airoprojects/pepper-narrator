"""
This script should listen to the ALMemory service and send the new state of game_info through the socket to the webpage api (?)
"""

import os
import qi
import sys
import time
import json
import socket 
import random
import subprocess
from copy import deepcopy


def format_dictionary_from_memory(item):
    dictionary = {}
    for key, val in item:
        if key in ['game_id', 'round', 'progressive_id']: val = int(val)
        dictionary[key] = val
    return dictionary

def connect_to_socket(ip_address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port))
    return client_socket

def send_info(client_socket, data):
    try:
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024)
        # if not response: client_socket.close()
        print("Received response:", response.decode('utf-8'))
        time.sleep(5)
    except Exception as e:
        client_socket.close() # to be on the safe side
        raise e
    
def votes_handler(response, game_state, game_info, memory):
    if game_state == 'voting_night':
        player_to_kill = int(max(response.items(), key=lambda item: item[1])[0])
        memory.insertData('votes', player_to_kill)
        print("player to kill: ", player_to_kill)
        print("votes: ", response)
    elif game_state == 'voting_day':
        votes = [0]*len(game_info['players'])
        for player, n_votes in response.items():
            votes[int(player)] = n_votes
        memory.insertData('votes', votes)

if __name__ == "__main__":

    # connection to python socket
    # local machine ip
    result = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True)
    ip_address = result.strip()
    print("local machine ip: ", ip_address)
    port = 65432 # generic
    client_socket = connect_to_socket(ip_address, port)
    
    # connection to naoqi robot
    robot_ip = '127.0.0.1' #'127.0.0.1'
    robot_port = 9559
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))
    print("session: ", session)
    memory = session.service("ALMemory")
    
    game_state_prev = None
    while True:
        game_state = memory.getData('game_state')

        if game_state != game_state_prev:
            game_info = format_dictionary_from_memory(memory.getData('game_info'))
            print("game state: ", game_state)
            print("game info: ", game_info)
            json_game_info = json.dumps(game_info)
            send_info(client_socket, json_game_info)
            response = json.loads( client_socket.recv(1024).decode('utf-8') )
            print("Received response:", response)
            print("not allowing other responses!!!")
            
            votes_handler(response, game_state, game_info, memory)
        else: 
            time.sleep(1)

        if memory.getData('state') == "end":  
            print("interrupting bridge connection!")
            break

    # closing connection
    client_socket.close()
    