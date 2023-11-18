from query_spotify_api import query_spotify
from api_constants import ARTISTS_ENDPOINT

def get_artists(artist_ids, access_token):
    ## Define artist data endpoint
    # Changes if querying one or multiple artists 
    endpoint = (f'{ARTISTS_ENDPOINT}/{artist_ids}' if isinstance(artist_ids, str) 
                else f'{ARTISTS_ENDPOINT}?ids={",".join(artist_ids)}')

    print(endpoint)
    print('Getting artists data...')

    artist_data = query_spotify(endpoint, access_token=access_token)    
    return artist_data