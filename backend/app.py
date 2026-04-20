from flask import Flask, request, jsonify
from flask_cors import CORS
import random
# import pandas as pd
# import os
from dotenv import load_dotenv
# from supabase import create_client, Client
from matrix import top_song, top_song_by_name
load_dotenv()


app = Flask(__name__)
CORS(app) 


@app.route('/')
def home():
    return "Flask API is running"

num_songs = 150
def randnums(numsongs):
    a = random.randint(0, numsongs - 1)
    b = random.randint(0, numsongs - 1)
    return a, b

# TODO
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"status": "Backend is running!", "port": 5000})
@app.route('/api/recommend', methods=['GET'])
def recommend():
    song = request.args.get("song")
    if not song:
        return jsonify({"error": "No song provided"}), 400
    print(f'Received request for song {song}')
 
    try:
        names = top_song_by_name(song, 9)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Song not found"}), 400
    print('found song_names', names)
    #recommendations = [audioMatrix.iloc[i]["name"] for i in indexes]
    return jsonify({"message": names})

@app.route('/api/random-songs', methods=['GET'])
def random_songs():
    # global idDict
    # a, b = randnums(10)
    # return jsonify({"song": str(idDict[a])})
    return jsonify({"message": "not defined yet"})


# TODO
@app.route('/api/compare', methods=['POST'])
def compare():
    return jsonify({"message": "not defined yet"})

if __name__ == '__main__':
    app.run()