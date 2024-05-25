

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
    

#"CALCULEMUSSSSSS"


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



if __name__ == '__main__':
    app.run(debug=True)






