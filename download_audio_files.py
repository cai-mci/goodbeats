import librosa
import yt_dlp
import numpy as np
import os
import pandas as pd
#~/Downloads/ffmpeg
#yt-dlp --ffmpeg-location "$HOME/Downloads/ffmpeg" URL
def extract_audio(youtube_url, year, rank):
    os.makedirs('audios', exist_ok=True)
    ydl_opts = {
        'format' : 'bestaudio/best',
        'download_archive': 'downloaded.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': f'audios/{year}/{rank}'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download= True)
        filename = f"audios/{year}/{rank}"
    
    y, sr = librosa.load(filename)
    mfccs = librosa.feature.mfcc(y=y, sr=sr).mean(axis=1)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr).mean(axis=1)
    tempo, _ =librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    zcr = librosa.feature.zero_crossing_rate(y).mean()

    return{
        'mfccs': mfccs, 'chroma' : chroma, 'tempo' : tempo, 'spectral_centroid' : spectral_centroid, 'zcr' : zcr
    }

df = pd.read_csv('top_50s_chart.csv')
urls = df.iloc[:,-1] #all rows and last col
yrs = df.iloc[:,0] #all rows, first column
ranks = df.iloc[:,1] #all rows, second column
#dataframe with all data
df2 = pd.DataFrame({
    'year':yrs,
    'rank':ranks,
    'url':urls
})
#filter for year>=2020
df2['year'] = pd.to_numeric(df2['year'], errors='coerce')
data = df2[df2['year']>=2020] 
print(data)
for i in range(len(data)):
    try:
        uloc = data.iloc[i]['url']
        yloc = data.iloc[i]['year']
        rloc = data.iloc[i]['rank']
        extract_audio(uloc,yloc,rloc)
    except:
        print("Skipping this video because of error")

    




