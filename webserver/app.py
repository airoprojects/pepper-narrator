# from flask import Flask, jsonify, send_from_directory
# import random

# app = Flask(__name__)

# # Endpoint to get the variable
# @app.route('/api/variable', methods=['GET'])
# def get_variable():
#     variable = random.randint(1, 100)  # Generating a random number as an example
#     return jsonify({'variable': variable})

# # Endpoint to serve the HTML file
# @app.route('/')
# def index():
#     return send_from_directory('', 'index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from threading import Thread
import time
from copy import deepcopy
import json
import os
from api import API
import subprocess

# Get the absolute path of the current project
script_path = os.path.abspath(__file__)
project_path = os.path.dirname(script_path) + '/../'
print(f"The directory containing this script is: {project_path}")

# global variables
game_info = {}  # Shared dictionary to store game info
player_vote = {}  # A dict that represents a votation on players; reset every votation
num_votes = 0

# Docker communication
result = subprocess.run("hostname -I | awk '{print $1}'", shell=True, capture_output=True, text=True)
ip_address = result.stdout.strip()
print(f"local machine ip: {ip_address}")
docker_api = API(host=ip_address, game_info=game_info)

# Flask app
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# service to get data from the webpage
@app.route('/submit_integer', methods=['POST'])
def submit_integer():
    global docker_api
    global num_votes
    global player_vote
    try:
        data = request.json
        print(f"recived data: {data}")

        if data is None:
            raise ValueError("No JSON data received")

        integer_value = data.get('integer', None)
        integer_value = int(integer_value)

        print("integer_value  ", integer_value)
        print("player_vote before ", player_vote)
        if integer_value not in player_vote.keys(): player_vote[integer_value] = 1
        else: player_vote[integer_value] += 1

        print(f"player_vote after: {player_vote}")
        num_votes += 1 
        print(f"number of votes: {num_votes}")

        print("max votes allowed: ", game_info["vote"].count(True))
        if num_votes == (game_info["vote"].count(True)):
            docker_api.send_back(player_vote)
            # reset voting
            num_votes = 0
            player_vote = {}
            print(f"reset num votes: {num_votes}")
            print(f"reset votes dictionary: {player_vote}")

        if integer_value is None or not isinstance(integer_value, int):
            raise ValueError("Invalid or missing integer")

        # Process the integer value as needed
        print(f"Received integer: {integer_value}")
        return jsonify({"status": "success", "integer": integer_value}), 200
    
    except Exception as e:
        print('catched error:', e)
        return jsonify({"status": "error", "message": str(e)}), 400


# Service to send data to the webpage
@app.route('/request_data')
def send_data():
    global game_info
    print(f"\nSending data: {game_info} to webpage")
    return jsonify(game_info)


# Endpoint to serve the HTML file
@app.route('/')
def index():
    return send_from_directory(project_path + 'webpage/', 'select_player.html')


# Endpoint to serve player.html
@app.route('/player.html')
def player():
    return send_from_directory(project_path + 'webpage/', 'player.html')

if __name__ == '__main__':
    
    docker_api.start_listening()
    # docker_api.start_connection()
    app.run(host='0.0.0.0', port=5000)
    
