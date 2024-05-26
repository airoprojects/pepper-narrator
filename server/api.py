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

@app.route('/get_data')
def send_data():
    global game_info, game_status
    data = {
        'game_info': game_info,
        'game_status': game_status
    }
    return jsonify(data)

@app.route('/request_status')
def send_status():
    global game_status
    data = {
        'game_status': game_status
    }
    return jsonify(data)

def listen(host, port):
    global game_info, game_status
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    s.bind((host, port))
    
    # Listen for incoming connections
    s.listen(1)
    
    print(f"Waiting for a connection... on port {port}")

    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received data:", data.decode('utf-8'))
            game_info = deepcopy(data.decode('utf-8'))
            
            # Update game_status based on game_info
            if 'active' in game_info:
                game_status = 'active'
            else:
                game_status = 'inactive'
            
            # Send a response
            conn.sendall("Data received".encode('utf-8'))

if __name__ == '__main__':
    # Socket configuration
    host = '0.0.0.0'
    port = 65432

    socket_thread = Thread(target=listen, args=(host, port))
    socket_thread.start()
    
    app.run(debug=True)