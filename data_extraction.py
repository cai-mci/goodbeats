import os
import warnings
import librosa
import numpy as np
import pandas as pd
from scipy import stats
import requests
from dotenv import load_dotenv
import sys

# MP3 downloads- will be found in /audios file

# TODO: create function to extract features from mp3 file
def columns ():
    feature_sizes = dict(chroma_stft=12, chroma_cqt=12, chroma_cens=12,
                         tonnetz=6, mfcc=12, rmse=1, zcr=1,
                         spectral_centroid=1, spectral_bandwidth=1,
                         spectral_contrast=7, spectral_rolloff=1)
    moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

    colums = []
    for name, size in feature_sizes.items():
        for moment in moments:
            it = ((name, moment, '{:02d}'.format(i+1)) for i in range(size))
            columns.extend(it)
    
    names = ('feature', 'statistics', 'number')
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    return columns.sort_values()

def compute_features(audio_path, year=None, rank=None, track_index=None):
    features = pd.Series(index=columns(), dtype='float32')
    warnings.filterwarnings('error', module='librosa')

    if year and rank:
        features["year"] = year
        features["rank"] = rank
    elif track_index:
        features["track_index"] = track_index

    def feature_stats(name, values):
        features[name, 'mean'] = np.mean(values, axis=1)
        features[name, 'std'] = np.std(values, axis=1)
        features[name, 'skew'] = stats.skew(values, axis=1)
        features[name, 'kurtosis'] = stats.kurtosis(values, axis=1)
        features[name, 'median'] = np.median(values, axis=1)
        features[name, 'min'] = np.min(values, axis=1)
        features[name, 'max'] = np.max(values, axis=1)
    
    try:
        filepath = audio_path
        x, sr = librosa.load(filepath, sr = None, mono = True)

        f = librosa.feature.zero_crossing_rate(x, frame_length = 2048, hop_length = 512)
        feature_stats('zcr', f)

        cqt = np.abs(librosa.cqt(x, sr = sr, hop_length = 512, bins_per_octave = 512, n_bins = 7*12, tuning = None))

        assert cqt.shape[0] == 7 * 12
        assert np.ceil(len(x)/512) <= cqt.shape[1] <= np.ceil(len(x)/512) + 1

        f = librosa.feature.chroma_cqt(C = cqt, n_chroma = 12, n_octaves = 7)
        feature_stats('chroma_cqt', f)
        f = librosa.feature.chroma_cens(C = cqt, n_chroma = 12, n_octaves = 7)
        feature_stats('chroma_cens', f)
        f = librosa.feature.tonnetz(chroma = f)
        feature_stats('tonnetz', f)

        del cqt
        stft = np.abs(librosa.stft(x, n_fft = 2048, hop_length = 512))
        assert stft.shape[0] == 1 + 2048 // 2
        assert np.ceil(len(x)/512) <= stft.shape[1] <= np.ceil(len(x)/512)+1
        del x

        f = librosa.feature.chroma_stft(S=stft**2, n_chroma = 12)
        feature_stats('chroma_stft', f)

        f = librosa.feature.rms(S=stft)
        feature_stats('rmse', f)

        f = librosa.feature.spectral_centroid(S = stft)
        feature_stats('spectral_centroid', f)
        f = librosa.feature.spectral_bandwidth(S = stft)
        feature_stats('spectral_bandwidth', f)
        f = librosa.feature.spectral_contrast(S = stft, n_bands = 6)
        feature_stats('spectral_contrast', f)
        f = librosa.feature.spectral_rolloff(S = stft)
        feature_stats('spectral_rolloff', f)

        mel = librosa.feature.melspectrogram(sr = sr, S = stft**2)
        del stft
        f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc = 20)
        feature_stats('mfcc', f)

    except Exception as e:
        print('{}: {}'.format(audio_path, repr(e)))

    return features

# TODO: create function to graph the extracted features 
# TODO: create function to normalize extracted features

print("hi")