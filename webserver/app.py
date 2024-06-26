from flask import Flask, request, jsonify, Response, send_from_directory, render_template
from flask_cors import CORS
from threading import Thread
import time
from copy import deepcopy
import json
import os
from api import API
import subprocess
import netifaces as ni

# Get the absolute path of the current project
script_path = os.path.abspath(__file__)
project_path = os.path.dirname(script_path) + "/" # '/../'
print(f"The directory containing this script is: {project_path}")

# global variables
game_info = {}  # Shared dictionary to store game info
player_vote = {}  # A dict that represents a votation on players; reset every votation
num_votes = 0

# Docker communication
interface_name = ni.gateways()['default'][ni.AF_INET][1] #ni.interfaces()[1]
ip_address = ni.ifaddresses(interface_name)[ni.AF_INET][0]['addr']
print(f"local machine ip: {ip_address}")
docker_api = API(host=ip_address, game_info=game_info)

# Flask app
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# service to get data from the webpage
@app.route('/submit_votes', methods=['POST'])
def submit_votes():
    global docker_api
    global num_votes
    global player_vote
    try:
        data = request.json
        print(f"recived data: {data}")

        if data is None:
            raise ValueError("No JSON data received")

        vote_id = data.get('vote', None)
        vote_id = int(vote_id)

        voter_id = data.get('voter', None)
        voter_id = int(voter_id)
        game_info['vote'][voter_id] = False

        print("integer_value  ", vote_id)
        print("player_vote before ", player_vote)
        if vote_id not in player_vote.keys(): player_vote[vote_id] = 1
        else: player_vote[vote_id] += 1

        print(f"player_vote after: {player_vote}")
        num_votes += 1 
        print(f"number of votes: {num_votes}")

        print("max votes allowed: ", docker_api.max_votes_allowed)
        if num_votes == docker_api.max_votes_allowed:
        #(game_info["vote"].count(True)):
            docker_api.send_back(player_vote)
            # reset voting
            num_votes = 0
            player_vote = {}
            print(f"reset num votes: {num_votes}")
            print(f"reset votes dictionary: {player_vote}")

        if vote_id is None or not isinstance(vote_id, int):
            raise ValueError("Invalid or missing integer")

        # Process the integer value as needed
        print(f"Received integer: {vote_id}")
        return jsonify({"status": "success", "integer": vote_id}), 200
    
    except Exception as e:
        print('catched error:', e)
        return jsonify({"status": "error", "message": str(e)}), 400


# Service to send data to the webpage
@app.route('/request_data')
def send_data():
    global game_info
    # print(f"\nSending data: {game_info} to webpage")
    return jsonify(game_info)


# Endpoint to serve environment.html
@app.route('/environment.html')
def environment():
    return render_template('environment.html', host_ip=ip_address)

# Endpoint to serve player_select.html
@app.route('/select_player.html')
def select_player():
    return render_template('select_player.html', host_ip=ip_address)

# Endpoint to serve player.html
@app.route('/player.html')
def player():
    return render_template('player.html', host_ip=ip_address)

# Endpoint to serve homepage
@app.route('/')
def index():
    return render_template('homepage.html', host_ip=ip_address)

if __name__ == '__main__':
    
    docker_api.start_listening()
    # docker_api.start_connection()
    app.run(host='0.0.0.0', port=5000)
    