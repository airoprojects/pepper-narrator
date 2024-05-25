
'''
TODO
# Create a new player by sending a POST request to /api/player with JSON data
'''

'''
The @ symbol in Python is used to denote a decorator.
\ A decorator is a special type of function that is used to modify the behavior of another function or method. 
In the context of Flask, decorators are used to define routes and handle HTTP requests.
# '''

# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Configure the SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# if __name__ == '__main__':
#     app.run(debug=True)
    

# "CALCULEMUSSSSSS"


from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


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
def get_data():
    data = {
        'message': 'Player eliminated',
        'number': 42
    }
    return jsonify(data)


import socket

# Configuration
host = '0.0.0.0'
port = 65432

def listen():
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
            
            # Send a response
            conn.sendall("Data received".encode('utf-8'))

if __name__ == '__main__':
    # app.run(debug=True)
    listen()






