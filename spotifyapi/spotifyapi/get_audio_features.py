from query_spotify_api import query_spotify
from api_constants import ARTISTS_ENDPOINT

def get_tracks_audio_features(track_ids, access_token):
    ## Define audio feature endpoint
    # Changes if querying one or multiple tracks 
    endpoint = (f'{AUDIO_FEATURES_ENDPOINT}/{track_ids}' if isinstance(track_ids, str) 
                else f'{AUDIO_FEATURES_ENDPOINT}?ids={",".join(track_ids)}')

    print(endpoint)
    print('Getting audio feature data...')

    audio_data = query_spotify(endpoint, access_token=access_token)    
    return audio_data