from query_spotify_api import query_spotify
from api_constants import ARTISTS_ENDPOINT

def get_artist_top_tracks(artist_id, access_token, market='US'):
    ## Define artist data endpoint
    endpoint = f'{ARTISTS_ENDPOINT}/{artist_id}/top-tracks?market={market}'
    print(endpoint)
    print('Getting track data...')

    track_data = query_spotify(endpoint, access_token=access_token)
    return track_data