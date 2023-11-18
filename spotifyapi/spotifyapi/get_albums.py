from query_spotify_api import query_spotify
from api_constants import ARTISTS_ENDPOINT

def get_artist_albums(artist_id, access_token, limit=10):
    ## Define artist data endpoint
    endpoint = f'{ARTISTS_ENDPOINT}{artist_id}/albums?limit={limit}'
    print('Getting album data...')

    album_data = query_spotify(endpoint, access_token=access_token)
    return album_data