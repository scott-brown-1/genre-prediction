## Data
DATA_DIR = './data'
ARTISTS_ENDPOINT = 'https://api.spotify.com/v1/artists'
AUDIO_FEATURES_ENDPOINT = 'https://api.spotify.com/v1/audio-features'

## Modeling
# NOTE: May want to convert release date to time series features (e.g. year, month, day, etc.)
DROP_COLS = ['Unnamed: 0','name','track_id','track_name','release_date','release_date_precision','Map','genres']