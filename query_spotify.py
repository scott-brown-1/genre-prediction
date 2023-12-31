import requests
from constants import ARTISTS_ENDPOINT, AUDIO_FEATURES_ENDPOINT

## Base API querying function for others to build on
def query_spotify(endpoint, access_token, timeout=60, retries=3):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    for i in range(retries):
        ## Handle timeout errors after 1 minute
        try:
            response = requests.get(endpoint, headers=headers, timeout=timeout)

            if response.status_code == 200:
                print('API request succeeded!')
                response_data = response.json()
                return response_data
            else:
                print(f'Request failed. Expected 200, got {response.status_code}: {response.text}')
                return None
        except requests.exceptions.Timeout as e:
            print(f'API request timed out: {e}')
            continue
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during the request: {e}')
            return None
    
    print('Failed to access API.')
    return None

def get_artists(artist_ids, access_token):
    ## Define artist data endpoint
    # Changes if querying one or multiple artists 
    endpoint = (f'{ARTISTS_ENDPOINT}/{artist_ids}' if isinstance(artist_ids, str) 
                else f'{ARTISTS_ENDPOINT}?ids={",".join(artist_ids)}')

    print(endpoint)
    print('Getting artists data...')

    artist_data = query_spotify(endpoint, access_token=access_token)    
    return artist_data

def get_artist_top_tracks(artist_id, access_token, market='US'):
    ## Define artist data endpoint
    endpoint = f'{ARTISTS_ENDPOINT}/{artist_id}/top-tracks?market={market}'
    print(endpoint)
    print('Getting track data...')

    track_data = query_spotify(endpoint, access_token=access_token)
    return track_data

def get_artist_albums(artist_id, access_token, limit=10):
    ## Define artist data endpoint
    endpoint = f'{ARTISTS_ENDPOINT}{artist_id}/albums?limit={limit}'
    print('Getting album data...')

    album_data = query_spotify(endpoint, access_token=access_token)
    return album_data

def get_tracks_audio_features(track_ids, access_token):
    ## Define audio feature endpoint
    # Changes if querying one or multiple tracks 
    endpoint = (f'{AUDIO_FEATURES_ENDPOINT}/{track_ids}' if isinstance(track_ids, str) 
                else f'{AUDIO_FEATURES_ENDPOINT}?ids={",".join(track_ids)}')

    print(endpoint)
    print('Getting audio feature data...')

    audio_data = query_spotify(endpoint, access_token=access_token)    
    return audio_data