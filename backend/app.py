from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()
supabase_url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
supabase_key = os.getenv('NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)
app = Flask(__name__)
CORS(app) 

import random
num_songs = 150
def randnums(numsongs):
    a = random.randint(0, numsongs - 1)
    b = random.randint(0, numsongs - 1)
    return a, b

# TODO
@app.route('/api/recommend', methods=['GET'])
def recommend():
    song = request.args.get("song")
    if not song:
        return jsonify({"error": "No song provided"}), 400
    response = supabase.table('Clean_Features').select("*").execute()
    songIndex = None
    #code right now is getting the song index
    audioMatrix =response.data.to_numpy()
    for i, row in enumerate(audioMatrix):
        if row[3].lower() == song.lower():
            songIndex = i
            break
    if songIndex is None:
        return jsonify({"error": "Song not found"}), 404

    #indexes = top_n_songs(songIndex, 10)
    recommendations = [audioMatrix.iloc[i]["name"] for i in range(10)]
    return jsonify({"message": recommendations})

# TODO
# data = pd.read_csv('Spotify_Song_Attributes.csv')
# columns_to_drop = ['artistName', 'msPlayed', 'type', 'id', 
#              'uri', 'track_href', 'analysis_url', 'genre']
# audioMatrix = data.drop(columns = columns_to_drop)
# audioFeaturesWithName = audioMatrix.to_numpy()

# idDict = {}
# #connecting to supabase to get data
# response = supabase.table('Clean_Features').select('*').execute()
# print(response)
# data = jsonify(response.data)

# print(data)
# for i in range(0, len(data)):
#     idDict[i] = data[i][3]
# print(idDict)
@app.route('/api/random-songs', methods=['GET'])
def random_songs():
    global idDict
    a, b = randnums(10)
    return jsonify({"song": str(idDict[a])})

# TODO
@app.route('/api/compare', methods=['POST'])
def compare():
    return jsonify({"message": "not defined yet"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)