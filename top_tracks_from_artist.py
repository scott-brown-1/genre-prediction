import time
import pandas as pd

from credentials import CLIENT_ID, CLIENT_SECRET
from constants import DATA_DIR

from access_tokens import get_access_token
from query_spotify import get_artist_top_tracks

QUERY_DELAY = 4 * 60 # minutes * seconds
MARKET = 'US'

## Get artist ids
artists = pd.read_csv(f'{DATA_DIR}/artists.csv')
artist_ids = artists.artist_id.values

## Loop through each artist
for i,artist_id in enumerate(artist_ids):
    ## Make sure access token is fresh 
    token = get_access_token(CLIENT_ID, CLIENT_SECRET, timeout = 60, retries = 3)
    
    ## Get artist top tracks from artist ids
    print('Getting tracks')

    track_res = get_artist_top_tracks(artist_id=artist_id, access_token=token, market=MARKET)
    if(track_res is None):
        print(f'Error getting artist {artist_id}')
        continue

    print(track_res)

    ## Clean response into dictionary
    track_res_clean = {
        'track_id': [track['id'] for track in track_res['tracks']],
        'track_name': [track['name'] for track in track_res['tracks']],
        'artist_id': [track['artists'][0]['id'] for track in track_res['tracks']],
        'artist_name': [track['artists'][0]['name'] for track in track_res['tracks']],
        'release_date': [track['album']['release_date'] for track in track_res['tracks']],
        'release_date_precision': [track['album']['release_date_precision'] for track in track_res['tracks']],
        'album_len': [track['album']['total_tracks'] for track in track_res['tracks']],
        'duration_ms': [track['duration_ms'] for track in track_res['tracks']],
        'explicit': [track['explicit'] for track in track_res['tracks']],
        'track_popularity': [track['popularity'] for track in track_res['tracks']]
    }
    
    ## Convert to dataframe and write to CSV
    print('Writing data to CSV...')
    track_data = pd.DataFrame.from_dict(track_res_clean)
    track_data.columns = track_res_clean.keys()
    track_data.to_csv(f'{DATA_DIR}/track_data.csv', mode='a', header=False, index=False)

    print(f'Finished chunk {i+1} of {len(artist_ids)}')
    time.sleep(QUERY_DELAY)