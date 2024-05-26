"""
This script should listen to the ALMemory service and send the new state of game_info through the socket to the webpage api (?)
"""

import os
import qi
import sys
import time
import socket 
import random
import json
from copy import deepcopy


def format_dictionary_from_memory(item):
    dictionary = {}
    for key, val in item:
        if key in ['game_id', 'round', 'progressive_id']: val = int(val)
        dictionary[key] = val
    return dictionary

def connect_to_socket(ip_address, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((ip_address, port))
    return my_socket

def send_info(my_socket, data):
    # try:
    my_socket.sendall(data.encode('utf-8'))
    response = my_socket.recv(1024)
    print("Received response:", response.decode('utf-8'))
    time.sleep(5)
    # finally:
    #     my_socket.close()

if __name__ == "__main__":

    # connection to python socket
    ip_address = '192.168.1.213' # IP address of Machine 2
    port = 65432
    my_socket = connect_to_socket(ip_address, port)
    
    # connection to naoqi robot
    robot_ip = '127.0.0.1' #'127.0.0.1'
    robot_port = 9559
    session = qi.Session()
    session.connect("tcp://{}:{}".format(robot_ip, robot_port))

    print(session)

    memory = session.service("ALMemory")
    game_info = dict()

    while True:
        # dictionary of the game
        game_info_update = format_dictionary_from_memory(memory.getData('game_info'))
        if game_info != game_info_update:
            game_info = game_info_update
            # print(game_info)
            json_game_info = json.dumps(game_info)
            send_info(my_socket, json_game_info)

        else: time.sleep(5)

        if memory.getData('state') == "end":  
            print("interrupting bridge connection!")
            break

    # closing connection
    my_socket.close()
    