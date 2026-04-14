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
                         tonnetz=6, mfcc=20, rmse=1, zcr=1,
                         spectral_centroid=1, spectral_bandwidth=1,
                         spectral_contrast=7, spectral_rolloff=1,
                         spectral_flatness=1,tempo=1, onset_strength=1,poly_features=3,
                          harmonic_rmse=1, percussive_rmse=1, pitch=2)
    moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

    columns = []
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
        # Ensure values is 2D (n_features, n_frames)
        if values.ndim == 1:
            values = values.reshape(1, -1)
        #calculate stats
        means = np.mean(values, axis=1)
        stds = np.std(values, axis=1)
        skews = stats.skew(values, axis=1)
        kurtoses = stats.kurtosis(values, axis=1)
        medians = np.median(values, axis=1)
        mins = np.min(values, axis=1)
        maxs = np.max(values, axis=1)
        #assign to series with proper indexing
        n_features = values.shape[0]
        for i in range(n_features):
            idx_num = f'{i+1:02d}'
            features[name, 'mean', idx_num] = means[i]
            features[name, 'std', idx_num] = stds[i]
            features[name, 'skew', idx_num] = skews[i]
            features[name, 'kurtosis', idx_num] = kurtoses[i]
            features[name, 'median', idx_num] = medians[i]
            features[name, 'min', idx_num] = mins[i]
            features[name, 'max', idx_num] = maxs[i]
    
    try:
        filepath = audio_path
        x, sr = librosa.load(filepath, sr = None, mono = True)
        #temp/beat features
        tempo, beat_frames = librosa.beat.beat_track(y=x, sr=sr)
        features['tempo', 'mean', '01'] = float(tempo)
        features['tempo', 'std', '01'] = 0.0
        #onset strength
        onset = librosa.onset.onset_strength(y=x, sr = sr)
        feature_stats('onset_strength', onset.reshape(1,-1))
        #zero crossing rate
        f = librosa.feature.zero_crossing_rate(x, frame_length = 2048, hop_length = 512)
        feature_stats('zcr', f)
        #cqt and chroma features
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
        #stft featuers
        stft = np.abs(librosa.stft(x, n_fft = 2048, hop_length = 512))
        assert stft.shape[0] == 1 + 2048 // 2
        assert np.ceil(len(x)/512) <= stft.shape[1] <= np.ceil(len(x)/512)+1
        
        #chroma stft
        f = librosa.feature.chroma_stft(S=stft**2, n_chroma = 12)
        feature_stats('chroma_stft', f)
        #rms (Energy)
        f = librosa.feature.rms(S=stft)
        feature_stats('rmse', f)
        #spectral features
        f = librosa.feature.spectral_centroid(S = stft)
        feature_stats('spectral_centroid', f)
        f = librosa.feature.spectral_bandwidth(S = stft)
        feature_stats('spectral_bandwidth', f)
        f = librosa.feature.spectral_contrast(S = stft, n_bands = 6)
        feature_stats('spectral_contrast', f)
        f = librosa.feature.spectral_rolloff(S = stft)
        feature_stats('spectral_rolloff', f)
        f = librosa.feature.spectral_flatness(y=x)
        feature_stats('spectral_flatness', f)
        #mfccs
        mel = librosa.feature.melspectrogram(sr = sr, S = stft**2)
        del stft
        f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc = 20)
        feature_stats('mfcc', f)
        #poly features
        poly_features = librosa.feature.poly_features(S=mel, order=2)
        feature_stats('poly_features', poly_features)
        #tempogram
        tempo_gram = librosa.feature.tempogram(y=x, sr=sr)
        #feature_stats('tempogram', tempo_gram)
        features['tempogram', 'mean', '01'] = np.mean(tempo_gram)
        features['tempogram', 'std', '01'] = np.std(tempo_gram)
        features['tempogram', 'max', '01'] = np.max(tempo_gram)
        features['tempogram', 'min', '01'] =np.min(tempo_gram)
        #harmonic and percussive
        harmonic, percussive = librosa.effects.hpss(x)
        harmonic_rmse = librosa.feature.rms(y=harmonic)
        percussive_rmse = librosa.feature.rms(y=percussive)
        feature_stats('harmonic_rmse', harmonic_rmse)
        feature_stats('percussive_rmse', percussive_rmse)
        #pitch features
        pitches, magnitudes = librosa.piptrack(y=x, sr=sr)
        pitch_mean = np.mean(pitches[pitches > 0])
        pitch_std = np.std(pitches[pitches > 0])
        features['pitch', 'mean', '01'] = pitch_mean
        features['pitch', 'std', '01'] = pitch_std
        del x
    except Exception as e:
        print('{}: {}'.format(audio_path, repr(e)))

    return features
df = pd.read_csv('top_50s_chart.csv')
urls = df.iloc[:,-1] #all rows and last col
yrs = df.iloc[:,0] #all rows, first column
ranks = df.iloc[:,1] #all rows, second column
names = df.iloc[:,2] #all rows, third column
artists = df.iloc[:,3]
#dataframe with all data
df2 = pd.DataFrame({
    'name':names,
    'artist': artists,
    'year':yrs,
    'rank':ranks,
    'url':urls
})
#filter for year>=2020
df2['year'] = pd.to_numeric(df2['year'], errors='coerce')
data = df2[df2['year']>=2020] 
def save_features(data, output = 'feature_stats_final.csv'):
    all_features = []
    if os.path.exists(output):
        curr_df = pd.read_csv(output)
        processed = set(zip(curr_df['year'],curr_df['rank']))
    else:
        processed = set()
        curr_df = None

    for i in range(len(data)):
        try:
            #uloc = data.iloc[i]['url']
            yloc = data.iloc[i]['year']
            rloc = data.iloc[i]['rank']
            name = data.iloc[i]['name']
            artist = data.iloc[i]['artist']
            url = data.iloc[i]['url']
            if (yloc, rloc) in processed:
                print("skipping",yloc,rloc)
                continue
            audio_path = f'audios/{yloc}/{rloc}.mp3'
            features = compute_features(audio_path)
            print("features computed", features)
            feature_df = features.to_frame().T
            #add metadata columns at beginning
            feature_df.columns = ['_'.join(col).strip() for col in feature_df.columns.values]
            feature_df.insert(0, 'url', url)
            feature_df.insert(0, 'artist', artist)
            feature_df.insert(0, 'name', name)
            feature_df.insert(0, 'rank', rloc)
            feature_df.insert(0, 'year', yloc)
            all_features.append(feature_df)
            if len(all_features)%10==0:
                csv_df = pd.concat(all_features, ignore_index=True)
                #flattening- look at this data later
                if curr_df is not None:
                    csv_df = pd.concat([curr_df, csv_df])
                os.makedirs('features', exist_ok = True)
                csv_df.to_csv(output, index = False)
            curr_df= csv_df
            print("Successfully got features")
        except:
            print("Skipping this video because of error")
    #save to csv
    if all_features:
        csv_df = pd.concat(all_features, ignore_index=True)
        #flattening- look at this data later
        csv_df.columns = ['_'.join(col).strip() for col in csv_df.columns.values]
        os.makedirs('features', exist_ok = True)
        csv_df.to_csv(output)
save_features(data)
