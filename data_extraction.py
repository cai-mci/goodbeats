import librosa
import yt_dlp
import numpy as np
import os
import pandas as pd
#~/Downloads/ffmpeg
#yt-dlp --ffmpeg-location "$HOME/Downloads/ffmpeg" URL
def extract_features(youtube_url):
    os.makedirs('audio', exist_ok=True)
    ydl_opts = {
        'format' : 'bestaudio/best',
        'outtmpl' : 'audio/%(title)s.%(ext)s',
        'download_archive': 'downloaded.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download= True)
        filename = f"audio/{info['title']}.mp3"
    
    y, sr = librosa.load(filename)
    mfccs = librosa.feature.mfcc(y=y, sr=sr).mean(axis=1)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr).mean(axis=1)
    tempo, _ =librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    zcr = librosa.feature.zero_crossing_rate(y).mean()

    return{
        'mfccs': mfccs, 'chroma' : chroma, 'tempo' : tempo, 'spectral_centroid' : spectral_centroid, 'zcr' : zcr
    }

failed = []
df = pd.read_csv('top_50s_chart.csv')
last = df.iloc[:,-1] #all rows and last col
for l in last:
    try:
        extract_features(l)
    except:
        print("Skipping this video because of error")
        failed.append(l)
    
