import requests
from api_constants import ARTISTS_ENDPOINT, AUDIO_FEATURES_ENDPOINT

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