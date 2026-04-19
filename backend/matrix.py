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


dataFrame = pd.read_csv('Clean_Features.csv')
# print(dataFrame.head())
drop = ['name_id', 'year', 'rank', 'url', 'artist']

fullSongData = dataFrame.to_numpy()
audioFeatures = dataFrame.drop(columns=drop)
audioMatrix = audioFeatures.drop(columns=['name']).to_numpy()
audioFeaturesWithName = audioFeatures.to_numpy()
# testSong1 = audioMatrix[0]
# testSong2 = audioMatrix[754]

idDict = {}
songDict = {}

for i in range(1, len(audioFeaturesWithName)):
    idDict[i] = audioFeaturesWithName[i][0]
    songDict[audioFeaturesWithName[i][0]] = i




# a = np.array([5, 4, 2])
# b = np.array([1111, 2222, 333333])
def cosine_similarity(song1, song2):
    bottom = norm(song1)*norm(song2)
    if bottom==0:
        return 0
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

testMatrix = [[""]]
testDict = {}
testSongFull = fullSongData[0]

#print(addSong, testSongFull, dataFrame['trackName'][0], testDict)
# print(testMatrix)

def top_song(song, n):
    similarity_scores = []
    for i in range(len(audioMatrix)):
        if i==song:
            continue
        song2Name = audioMatrix[i][3]
        print(song2Name)
        similarity_scores.append(cosine_similarity(audioMatrix[song], audioMatrix[i]))
    #list of score index pairs
    scored_idx = [(score, idx) for idx, score in enumerate(similarity_scores)]
    scored_idx.sort(reverse=True)
    if n >= len(similarity_scores):
        return [idx+1 for _,idx in scored_idx]
    else:
        return [idx+1 for _,idx in scored_idx[:n]]
def top_song_by_name(song_name,n):
    song_index = songDict[song_name]
    similar_idxs = top_song(song_index, n+1)
    return similar_idxs

#print(top_song(1, 10))