from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import time
from copy import deepcopy
from threading import Thread

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

game_info = {}  # Shared dictionary to store game info
game_status = 'inactive'  # Initial game status

player_vote = dict()  # A dict that represents a votation on players; reset every votation

@app.route('/submit_integer', methods=['POST'])
def submit_integer():
    try:
        data = request.json
        if data is None:
            raise ValueError("No JSON data received")

        integer_value = data.get('integer', None)
        
        if integer_value is None or not isinstance(integer_value, int):
            raise ValueError("Invalid or missing integer")

        # Process the integer value as needed
        print(f"Received integer: {integer_value}")
        return jsonify({"status": "success", "integer": integer_value}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/request_data')
def send_data():
    global game_info
    data = {
        "info": game_info
    }
    print(f"\nSending data: {game_info} to webpage")
    return game_info

def listen(host, port):
    global game_info
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Waiting for a connection... on port {port}")

    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            print(f"\nReceived data: {data.decode('utf-8')} \n")
            game_info = deepcopy(data.decode('utf-8'))
            
            # Send a response
            conn.sendall("Data received".encode('utf-8'))

if __name__ == '__main__':
    # Socket configuration
    host = '0.0.0.0'
    port = 65432

    socket_thread = Thread(target=listen, args=(host, port))
    socket_thread.start()
    
    app.run(debug=False)