import csv

with open('Spotify_Song_Attributes.csv', mode='r', newline='', encoding='utf-8') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    for row in csv_reader:
        print(row)
        break
