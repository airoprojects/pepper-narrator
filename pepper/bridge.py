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

if __name__ == "__main__":

    # connection to python socket
    # local machine ip
    result = result = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True)
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
    game_info = dict()

    while True:
        game_info_update = format_dictionary_from_memory(memory.getData('game_info'))

        if game_info != game_info_update:
            game_info = game_info_update
            print("game info: ", game_info)
            json_game_info = json.dumps(game_info)
            send_info(client_socket, json_game_info)
            response = client_socket.recv(1024)
            print("Received response:", response.decode('utf-8'))
            print("not allowing other responses!!!")
        else: 
            time.sleep(5)

        if memory.getData('state') == "end":  
            print("interrupting bridge connection!")
            break

    # closing connection
    client_socket.close()
    