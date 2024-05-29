# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_sse import sse
# import socket
# import time
# from copy import deepcopy
# from threading import Thread
# import json

# app = Flask(__name__)
# CORS(app)  # This will enable CORS for all routes
# app.config["REDIS_URL"] = "redis://localhost:6379"
# app.register_blueprint(sse, url_prefix='/stream')

# # global variables
# game_info = {}  # Shared dictionary to store game info
# game_status = 'inactive'  # Initial game status
# player_vote = dict()  # A dict that represents a votation on players; reset every votation
# num_votes = 0

# def make_socket(host, port):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(1)
#     print(f"Waiting for a connection... on port {port}")
#     # conn, addr = server_socket.accept()
#     return server_socket

# # Socket configuration
# host = '0.0.0.0'
# port = 65432
# server_socket = make_socket(host, port)
# conn, addr = server_socket.accept()


# def listen():
#     global conn
#     global game_info
#     global num_votes
  
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data: break
#             print(f"\nReceived data: {data.decode('utf-8')} \n")
#             game_info = deepcopy(data.decode('utf-8'))
#             conn.sendall("Data received".encode('utf-8'))
#             game_info = json.loads(game_info)


# def send_back():
#     global conn
#     global num_votes
#     global player_vote
#     print("Sending data to bridge")
#     send_data = json.dumps(player_vote)
#     conn.sendall(send_data.encode('utf-8'))
#     # reset player vot dictionary
#     num_votes = 0 
#     player_vote = {}


# # @app.route('/voto_enabling')
# # def 

# # Server Flask
# @app.route('/submit_integer', methods=['POST'])
# def submit_integer():
#     global num_votes
#     try:
#         data = request.json
#         print("ciaoooo   ",data)

#         if data is None:
#             raise ValueError("No JSON data received")

#         integer_value = data.get('integer', None)
#         integer_value = int(integer_value)

#         print("integer_value  ", integer_value)
#         print("player_vote before ",player_vote)
#         if integer_value not in player_vote.keys(): player_vote[integer_value] = 1
#         else: player_vote[integer_value] += 1

#         print("player_vote after ",player_vote)
#         num_votes += 1 

#         if num_votes == (game_info["vote"].count(True)): send_back()

#         print(f"number of votes: {num_votes}")
#         print(f"votes dictionary: {player_vote}")
        
#         if integer_value is None or not isinstance(integer_value, int):
#             raise ValueError("Invalid or missing integer")

#         # Process the integer value as needed
#         print(f"Received integer: {integer_value}")
#         return jsonify({"status": "success", "integer": integer_value}), 200
    
#     except Exception as e:
#         print('errore:',e)
#         return jsonify({"status": "error", "message": str(e)}), 400


# @app.route('/request_data')
# def send_data():
#     global game_info
#     print(f"\nSending data: {game_info} to webpage")
#     return jsonify(game_info)


# if __name__ == '__main__':

#     socket_thread = Thread(target=listen, args=())
#     socket_thread.start()
    
#     app.run(debug=False)







##PROVA

from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from flask_sse import sse
import socket
import time
from copy import deepcopy
from threading import Thread
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Ensure Redis URL is configured correctly
# app.config["REDIS_URL"] = "redis://localhost:6379"
# app.register_blueprint(sse, url_prefix='/stream')

# global variables
game_info = {}  # Shared dictionary to store game info
game_status = 'inactive'  # Initial game status
player_vote = dict()  # A dict that represents a votation on players; reset every votation
num_votes = 0

def make_socket(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Waiting for a connection... on port {port}")
    return server_socket

# Socket configuration
host = '0.0.0.0'
port = 65432
server_socket = make_socket(host, port)
conn, addr = server_socket.accept()

def listen():
    global conn
    global game_info
    global num_votes

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"\nReceived data: {data.decode('utf-8')} \n")
            game_info = deepcopy(data.decode('utf-8'))
            conn.sendall("Data received".encode('utf-8'))
            game_info = json.loads(game_info)

            with app.app_context():
                # Notify all clients about the new game_info
                sse.publish({"game_info": game_info}, type='game_update')

def send_back():
    global conn
    global num_votes
    global player_vote
    print("Sending data to bridge")
    send_data = json.dumps(player_vote)
    conn.sendall(send_data.encode('utf-8'))
    # reset player vote dictionary
    num_votes = 0 
    player_vote = {}

@app.route('/submit_integer', methods=['POST'])
def submit_integer():
    global num_votes
    try:
        data = request.json
        print("ciaoooo   ",data)

        if data is None:
            raise ValueError("No JSON data received")

        integer_value = data.get('integer', None)
        integer_value = int(integer_value)

        print("integer_value  ", integer_value)
        print("player_vote before ",player_vote)
        if integer_value not in player_vote.keys(): player_vote[integer_value] = 1
        else: player_vote[integer_value] += 1

        print("player_vote after ",player_vote)
        num_votes += 1 

        if num_votes == (game_info["vote"].count(True)): send_back()

        print(f"number of votes: {num_votes}")
        print(f"votes dictionary: {player_vote}")

        if integer_value is None or not isinstance(integer_value, int):
            raise ValueError("Invalid or missing integer")

        # Process the integer value as needed
        print(f"Received integer: {integer_value}")
        return jsonify({"status": "success", "integer": integer_value}), 200
    
    except Exception as e:
        print('errore:', e)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/request_data',  methods=['GET'])
def send_data():
    global game_info
    print(f"\nSending data: {game_info} to webpage")
    return jsonify(game_info)

# @app.route('/stream')
# def stream():
#     def event_stream():
#         pubsub = sse.pubsub()
#         pubsub.subscribe('game_update')
#         for message in pubsub.listen():
#             if message['type'] == 'message':
#                 yield f"data: {message['data']}\n\n"
#     return Response(event_stream(), content_type='text/event-stream')

# Endpoint to serve the HTML file
@app.route('../clients/')
def index():
    return send_from_directory('', 'select_players.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    # socket_thread = Thread(target=listen, args=())
    # socket_thread.start()