from flask import Flask, jsonify, send_from_directory
import random

app = Flask(__name__)

# Endpoint to get the variable
@app.route('/api/variable', methods=['GET'])
def get_variable():
    variable = random.randint(1, 100)  # Generating a random number as an example
    return jsonify({'variable': variable})

# Endpoint to serve the HTML file
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)