import pandas as pd
import numpy as np

# dataFrame = pd.read_csv('Spotify_Song_Attributes.csv')
# print(dataFrame.head())
# matrixData = dataFrame.to_numpy()
# print(matrixData)


import csv

with open('Spotify_Song_Attributes.csv', mode='r', newline='', encoding='utf-8') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    for row in csv_reader:
        print(row)
        break

