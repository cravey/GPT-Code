import requests
import sys

# Replace with your client ID and secret
CLIENT_ID = 'client_id_goes_here'
CLIENT_SECRET = 'client_secret_goes_here'

def get_oauth_token():
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    
    response = requests.post(url, params=payload)
    data = response.json()
    return data["access_token"]

def get_user_broadcaster_type(username, oauth_token):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {oauth_token}"
    }
    
    response = requests.get(f"https://api.twitch.tv/helix/users?login={username}", headers=headers)
    data = response.json()
    
    users = data.get("data", [])
    if not users:
        return None

    return users[0].get("broadcaster_type")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <twitch_username>")
        sys.exit(1)
    
    username = sys.argv[1]
    token = get_oauth_token()
    broadcaster_type = get_user_broadcaster_type(username, token)
    
    if broadcaster_type:
        print(f"{username} is a Twitch {broadcaster_type}.")
    else:
        print(f"{username} is neither an affiliate nor a partner.")
