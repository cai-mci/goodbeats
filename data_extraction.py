import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import librosa
import yt_dlp
import numpy as np

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id or not client_secret:
    raise RuntimeError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env file")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

def extract_features(youtube_url):

    os.makedirs('audio', exist_ok=True)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'outtmpl' : 'audio/%(title)s.%(ext)s',
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
    
    
