import pandas as pd
import numpy as np
from numpy.linalg import norm

dataFrame = pd.read_csv('test_data/Spotify_Song_Attributes.csv')

columns_to_drop = ['artistName', 'msPlayed', 'type', 'id', 
             'uri', 'track_href', 'analysis_url', 'genre']

audioMatrix = dataFrame.drop(columns = columns_to_drop)
audioFeatures = audioMatrix.drop(columns=['trackName']).to_numpy()
audioFeaturesWithName = audioMatrix.to_numpy()

idDict = {}
songDict = {}

for i in range(1, len(audioFeaturesWithName)):
    idDict[i] = audioFeaturesWithName[i][0]
    songDict[audioFeaturesWithName[i][0]] = i


def cosine_similarity(song1, song2):
    denom = (norm(song1) * norm(song2))
    if(denom == 0):
        return 0
    cosine = np.dot(song1, song2) / denom
    return cosine


def top_n_songs(song_index, n):
    similarity_scores = []

    for i in range(0, len(audioFeatures)):
        if(i == song_index):
            continue
        
        similarity_scores.append((i,cosine_similarity(audioFeatures[song_index], audioFeatures[i])))


    values = sorted(similarity_scores, key = lambda x: x[1], reverse = True)[:n]

    
    return [i for i,_ in values]

print(top_n_songs(1, 4))
