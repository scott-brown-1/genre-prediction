print('Script init')

## Imports and Setup
import requests
import pandas as pd
import time
from credentials import CLIENT_ID, CLIENT_SECRET # TEMPORARY WORKAROUND
from constants import DATA_DIR

from access_tokens import get_access_token
from query_spotify import get_artists
from utils import chunk_list

CHUNK_SIZE = 50 # artists per query
QUERY_DELAY = 240 # 6 mins in seconds

## Get artist ids
artists = pd.read_csv(f'{DATA_DIR}/artists.csv')
artist_chunks = chunk_list(artists.artist_id.values, CHUNK_SIZE)

## Loop through each chunk of artists
for i,ids in enumerate(artist_chunks):
    ## Make sure access token is fresh
    token = get_access_token(CLIENT_ID, CLIENT_SECRET, timeout = 60, retries = 3)
    
    ## Get artist data from ids
    print('Getting artists')
    artist_res = get_artists(ids, access_token = token)
    if(artist_res is None):
        print(f'Error getting batch')
        continue
    
    ## Clean response into dictionary
    artist_res_clean = {
        'artist_id': [artist['id'] for artist in artist_res['artists']],
        'name': [artist['name'] for artist in artist_res['artists']],
        'genres': [','.join(artist['genres']) for artist in artist_res['artists']],
        'popularity': [artist['popularity'] for artist in artist_res['artists']],
        'followers': [artist['followers']['total'] for artist in artist_res['artists']]
    }

    ## Convert to dataframe and write to CSV
    print('Writing data to CSV...')
    artist_data = pd.DataFrame.from_dict(artist_res_clean)
    artist_data.columns = artist_res_clean.keys()

    keep_header = True if i == 0 else False
    artist_data.to_csv(f'{DATA_DIR}/artist_data.csv', mode='a', header=keep_header, index=False)

    print(f'Finished chunk {i} of {len(artists.artist_id.values) // CHUNK_SIZE + 1}')
    time.sleep(QUERY_DELAY)

print('Script complete')
