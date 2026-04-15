import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import random
import supabase

app = Flask(__name__)
CORS(app) 

#initialize Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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
    data = request.json

    #extract data sent from frontend
    user_id = data.get('user_id')
    song_a_id = 0 #data.get('song_a_id')
    song_b_id = 1 #data.get('song_b_id')

    rating = data.get('rating') #expecting -2 (strongly disagree) to 2 (strongly agree)

    if rating is None or not (-2 <= int(rating) <= 2):
        return jsonify({"error": "Invalid rating. Must be between -2 and 2."}), 400
    
    try:
        #insert into song_comparison
        response = supabase.table("song_comparison").insert({
            "user": user_id,      
            "song_a": song_a_id,   
            "song_b": song_b_id,    
            "rating": rating      
        }).execute()

        return jsonify({
            "status": "success", 
            "message": f"Comparison saved for user {user_id}",
            "data": response.data
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)