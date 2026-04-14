from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app) 

# TODO
@app.route('/api/recommend', methods=['GET'])
def recommend():
    return jsonify({"message": "not defined yet"})

# TODO
@app.route('/api/random-songs', methods=['GET'])
def random_songs():
    return jsonify({"message": "not defined yet"})

# TODO
@app.route('/api/compare', methods=['POST'])
def compare():
    return jsonify({"message": "not defined yet"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)