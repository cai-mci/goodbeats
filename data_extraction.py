import os
import requests
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

# MP3 downloads
import yt_dlp as youtube_dl
from __future__ import unicode_literals

load_dotenv()

api_url = os.getenv("SPOTIFY_CLIENT_ID")
base_url = os.getenv("SPOTIFY_REDIRECT_URI")

if not api_url or not base_url:
    raise RuntimeError("Missing API_URL or BASE_URL check .env file")

def get_music_features(track_url):
    track_id = track_url.split(':')[-1].split('/')[-1].split('?')[0]

    audio_features = sp.audio_features([track_id])[0]


# TODO: create function to extract features from mp3 file

print("hi")