import pandas as pd
import numpy as np
from numpy.linalg import norm
import csv

# with open('Spotify_Song_Attributes.csv', mode='r', newline='', encoding='utf-8') as file:
#     # Create a CSV reader object
#     csv_reader = csv.reader(file)

#     for row in csv_reader:
#         print(row)
#         break


dataFrame = pd.read_csv('Spotify_Song_Attributes.csv')
# print(dataFrame.head())
drop = ['trackName', 'artistName', 'msPlayed', 'type', 'id', 
             'uri', 'track_href', 'analysis_url', 'genre']
audioFreatures = dataFrame.drop(columns=drop)
#print(audioFreatures)
audioMatrix = audioFreatures.to_numpy()
testSong1 = audioMatrix[0]
testSong2 = audioMatrix[754]

a = np.array([5, 4, 2])
b = np.array([1111, 2222, 333333])
def cosine_similarity(song1, song2):
    cosine = np.dot(song1, song2) / (norm(song1) * norm(song2))
    return cosine

print(cosine_similarity(a, b))
