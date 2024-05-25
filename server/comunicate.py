

'''
TODO
# Create a new player by sending a POST request to /api/player with JSON data

'''

'''
The @ symbol in Python is used to denote a decorator.
\ A decorator is a special type of function that is used to modify the behavior of another function or method. 
In the context of Flask, decorators are used to define routes and handle HTTP requests.
'''

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Player {self.name}>'

# Create the database and the Player table
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint to insert a new player
@app.route('/api/player', methods=['POST'])
def add_player():
    data = request.get_json()
    new_player = Player(name=data['name'], role=data['role'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({'message': 'Player added successfully'}), 201

# Endpoint to get all players
@app.route('/api/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    player_list = [{'id': player.id, 'name': player.name, 'role': player.role} for player in players]
    return jsonify(player_list)

# Endpoint to delete a player
@app.route('/api/player/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = Player.query.get(player_id)
    if player is None:
        return jsonify({'message': 'Player not found'}), 404
    
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Player deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
    





