print('Script init')

import time
import pandas as pd

from credentials import CLIENT_ID, CLIENT_SECRET # TEMPORARY WORKAROUND
from constants import DATA_DIR

from access_tokens import get_access_token
from query_spotify import get_tracks_audio_features
from utils import chunk_list

CHUNK_SIZE = 50 # tracks per query
QUERY_DELAY = 60*3 # 3 mins in seconds

## Get track ids
tracks = pd.read_csv(f'{DATA_DIR}/track_data.csv')
track_chunks = chunk_list(tracks.track_id.values, CHUNK_SIZE)
n_chunks = len(tracks.track_id.values) // CHUNK_SIZE

## Loop through each chunk of tracks
for i,ids in enumerate(track_chunks):
    ## Make sure access token is fresh
    token = get_access_token(CLIENT_ID, CLIENT_SECRET, timeout = 60, retries = 3)
    
    ## Get artist data from ids
    print('Getting tracks')
    audio_res = get_tracks_audio_features(ids, access_token = token)
    if(audio_res is None):
        print('Error getting batch')
        continue
    
    ## Clean response into dictionary
    audio_res_clean = {
        'track_id': [audio['id'] for audio in audio_res['audio_features']],
        'danceability': [audio['danceability'] for audio in audio_res['audio_features']],
        'energy': [audio['energy'] for audio in audio_res['audio_features']],
        'key': [audio['key'] for audio in audio_res['audio_features']],
        'loudness': [audio['loudness'] for audio in audio_res['audio_features']],
        'mode': [audio['mode'] for audio in audio_res['audio_features']],
        'speechiness': [audio['speechiness'] for audio in audio_res['audio_features']],
        'acousticness': [audio['acousticness'] for audio in audio_res['audio_features']],
        'instrumentalness': [audio['instrumentalness'] for audio in audio_res['audio_features']],
        'liveness': [audio['liveness'] for audio in audio_res['audio_features']],
        'valence': [audio['valence'] for audio in audio_res['audio_features']],
        'tempo': [audio['tempo'] for audio in audio_res['audio_features']],
        'time_signature': [audio['time_signature'] for audio in audio_res['audio_features']],
    }

    ## Convert to dataframe and write to CSV
    print('Writing data to CSV...')
    audio_data = pd.DataFrame.from_dict(audio_res_clean)
    audio_data.columns = audio_res_clean.keys()

    keep_header = True if i == 0 else False
    audio_data.to_csv(f'{DATA_DIR}/audio_feature_data.csv', mode='a', header=keep_header, index=False)

    print(f'Finished chunk {i+1} of {n_chunks+1}')
    time.sleep(QUERY_DELAY)

print('Script complete')