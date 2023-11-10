## Imports and Setup
import requests
import pandas as pd
import time
from credentials import CLIENT_ID, CLIENT_SECRET # TEMPORARY WORKAROUND
from constants import DATA_DIR

from access_tokens import get_access_token
from query_spotify import get_artists

CHUNK_SIZE = 50 # artists per query
QUERY_DELAY = 5 # seconds

## Function to break ids into chunks
def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

## Get artist ids
artists = pd.read_csv(f'{DATA_DIR}/artists.csv')
artist_chunks = chunk_list(artists.artist_id.values, CHUNK_SIZE)

for i,ids in enumerate(artist_chunks):
    # TODO: wait for response from this line before proceeding?
    token = get_access_token(CLIENT_ID, CLIENT_SECRET, timeout = 60, retries = 3)
    
    print('Getting artists')
    artist_res = get_artists(ids, access_token = token)
    
    artist_res_clean = {
        'artist_id': [artist['id'] for artist in artist_res['artists']],
        'name': [artist['name'] for artist in artist_res['artists']],
        'genres': [','.join(artist['genres']) for artist in artist_res['artists']],
        'popularity': [artist['popularity'] for artist in artist_res['artists']],
        'followers': [artist['followers']['total'] for artist in artist_res['artists']]
    }

    print('Writing data to CSV...')
    artist_data = pd.DataFrame.from_dict(artist_res_clean)
    artist_data.to_csv(f'{DATA_DIR}/artist_data.csv', mode='a', header=False, index=False)
    artist_data.columns = artist_res_clean.keys()

    print(f'Finished chunk {i} of {len(artists.artist_id.values) // CHUNK_SIZE + 1}')
    time.sleep(QUERY_DELAY)