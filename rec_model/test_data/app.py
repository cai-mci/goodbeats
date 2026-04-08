import json
from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

data_file = 'Spotify_Song_Attributes.csv'
df = pd.read_csv(data_file)


#print(df.columns.tolist())
#print(df.head(2))

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/song/<id>', methods = ['GET'])
def get_song(id):
    result = df[df['id'] == id]
    if result.empty:
        return jsonify({ 'error': 'Employee does not exist'}), 404
    song = result.iloc[0]
    return jsonify({
        'id': song['id'],
        'trackName': song['trackName'],
        'artistName': song['artistName'],
    }) 

if __name__ == '__main__':
    app.run(debug=True)
