"""
This script should listen to the ALMemory service and send the new state of game_info through the socket to the webpage api (?)
"""

import os
import qi
import sys
import time
import socket 
import random
from copy import deepcopy

# Configuration
local_server_address = 'localhost'
local_server_port = 12345
fixed_ip_address = '192.168.1.213' # IP address of Machine 2
port = 65432

def read_data_from_local_server():
    # Dummy data for example
    return "Hello from Python 2.7 inside Docker"

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((fixed_ip_address, port))
    
    try:
        while True:
            data = read_data_from_local_server()
            s.sendall(data.encode('utf-8'))
            response = s.recv(1024)
            print("Received response:", response.decode('utf-8'))
            time.sleep(5)
    finally:
        s.close()

if __name__ == "__main__":
    main()