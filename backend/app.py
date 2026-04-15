from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app) 

import random

def randnums(numsongs):
    a = random.randint(0, numsongs - 1)
    b = random.randint(0, numsongs - 1)
    return a, b

# TODO
@app.route('/api/recommend', methods=['GET'])
def recommend():
    return jsonify({"message": "not defined yet"})

# TODO
@app.route('/api/random-songs', methods=['GET'])
def random_songs():
    a, b = randnums(10)
    return jsonify({"message": "{a}, {b}"})

# TODO
@app.route('/api/compare', methods=['POST'])
def compare():
    return jsonify({"message": "not defined yet"})

@app.route('/api/signup', methods=['POST'])
def signup():
    
    return jsonify({"message": "not defined yet"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)