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
drop = ['artistName', 'msPlayed', 'type', 'id', 
             'uri', 'track_href', 'analysis_url', 'genre']
fullSongData = dataFrame.to_numpy()
audioFeatures = dataFrame.drop(columns=drop)
audioMatrix = audioFeatures.drop(columns=['trackName']).to_numpy()
testSong1 = audioMatrix[0]
testSong2 = audioMatrix[754]

# a = np.array([5, 4, 2])
# b = np.array([1111, 2222, 333333])
def cosine_similarity(song1, song2):
    cosine = np.dot(song1, song2) / (norm(song1) * norm(song2))
    return cosine

# print(cosine_similarity(a, b))

# testMatrix = []
# dataFrameDict = dataFrame.set_index('trackName').to_dict(orient='index')
# print(dataFrameDict)

# Adding to Similarity Matrix
# def add_to_matrix(matrix, song):
#     matrix.append(np.array(song))

# add_to_matrix(testMatrix, testSong1)
# add_to_matrix(testMatrix, testSong2)

testMatrix = [[]]
testDict = {}
testSongFull = fullSongData[0]
def addSong(matrix: list, song: list, songName: str, dict: dict):
    dict[songName] = song

    matrix.append(songName)
    matrix[0].append(songName)

    for i in range(1, len(matrix[0])):
        song2Name = matrix[0][i]
        matrix[len(matrix) - 1].append(cosine_similarity(song,dict[song2Name]))

    return matrix

print(addSong([""], [1,0,2,0,3,1], "song", {}))
#print(addSong, testSongFull, dataFrame['trackName'][0], testDict)
# print(testMatrix)

def top_song(song, n):
    similarity_scores = sim_matrix[song]
    if n >= len(similarity_scores):
        indexes = []
        for i in similarity_scores:
            indexes.append(similarity_scores.index(i))
        return indexes
    else:
        values = sorted(similarity_scores, reverse = True)[:n]
        indexes = []
        for i in values:
            indexes.append(values.index(i))
        return indexes

print(top_song(1, 4))