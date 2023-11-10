import requests
import json
import datetime
        
def get_new_access_token(client_id, client_secret, timeout=60, retries=3):
    ## Define API endpoint and data
    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    for i in range(retries):
        try:
            ## Query API
            response = requests.post(url, headers=headers, data=data, timeout=timeout)

            if response.status_code == 200:
                ## If request is successful, calc expire time and return response data
                print('API request succeeded!')
                print(response.json())
                res_data = response.json()

                ## Calculate expire time from expires_in parameter (which is in seconds)
                res_data['expire_date'] = datetime.datetime.now().timestamp() + response.json()['expires_in']

                return res_data
            else:
                ## Otherwise, print error
                print(f'Request failed. Expected 200, got {response.status_code}: {response.text}')
                return None
        except requests.exceptions.Timeout as e:
            print(f'API request timed out: {e}')
            continue
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during the request: {e}')
            return None
        
    print('Failed to get access token.')
    return None
    
def get_access_token(client_id, client_secret, timeout=60, retries=3):
    token_file_path = 'access_token.json'
    try:
        with open(token_file_path, 'r') as token_file:
            data = json.load(token_file)

        ## If token expires in the next 2 minutes, get new token
        if data['expire_date'] < datetime.datetime.now().timestamp() + 120:
            ## Get new token and write to file
            print('Token expired. Getting new token...')
            response = get_new_access_token(
                client_id = client_id, 
                client_secret = client_secret,
                timeout = timeout,
                retries = retries)

            with open(token_file_path, 'w') as token_file:
                json.dump(response, token_file)

            return response['access_token']
        else:
            ## Otherwise, get existing token
            print('Using existing token...')
            return data['access_token']
    except FileNotFoundError:
        print(f'{token_file_path} not found.')