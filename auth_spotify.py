import requests
from bs4 import BeautifulSoup
import webbrowser
from urllib.parse import urlencode
import base64
from dotenv import load_dotenv
import os

load_dotenv()
# Create a .env file in root directory for all API keys and tokens

CLIENT_ID_SPOTIFY = os.environ.get("CLIENT_ID_SPOTIFY")
SECRET_ID_SPOTIFY = os.environ.get("SECRET_ID_SPOTIFY")
ENDPOINT_SPOTIFY = 'https://accounts.spotify.com/authorize'
REDIRECT_URI = "https://example.com/calback"
SCOPE = "playlist-modify-private"

ENDPOINT_SPOTIFY_TOKEN = "https://accounts.spotify.com/api/token"
ENCODED = base64.b64encode((CLIENT_ID_SPOTIFY + ":" + SECRET_ID_SPOTIFY).encode("ascii")).decode("ascii")

class SpotifyAuth:

    def __init__(self):
        self.acces_token = ""
        self.refresh_token = ""

    def auth_token(self):
        """ Authentication with OAuth2
            copy the code from the callback URI
            then returns token"""

        auth_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Basic " + ENCODED
        }
        params_auth = {
            "response_type": "code",
            "client_id": CLIENT_ID_SPOTIFY,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPE
        }

        webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(params_auth))
        CODE = str(input("enter your code here: "))

        response_auth = requests.get(url=ENDPOINT_SPOTIFY, params=params_auth)
        print(response_auth.status_code)

        data_token = {
            "code": CODE,
            "redirect_uri": REDIRECT_URI,
            "grant_type": 'authorization_code'
        }

        response_token = requests.post(url=ENDPOINT_SPOTIFY_TOKEN, data=data_token, headers=auth_headers)
        print(response_token.status_code)
        data = response_token.json()
        self.acces_token = data["access_token"]
        refresh_token = data["refresh_token"]
        print(self.acces_token)
        return self.acces_token

    def auth_refresh_token(self):

        auth_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   "Authorization": "Basic " + ENCODED}
        data_token = {
            "refresh_token": self.refresh_token,
            "grant_type": 'refresh_token'
        }

        response_token = requests.post(url=ENDPOINT_SPOTIFY_TOKEN, data=data_token, headers=auth_headers)
        print(response_token.status_code)
        data = response_token.json()
        self.acces_token = data["access_token"]
        print(acces_token)
        return self.acces_token

    def search_track(self, song, artist, token):

        url_search_track = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        query = {
            "q": f"{song}+{artist}",
            "type": "track,artist",
            "market": "RO"
        }
        response_track = requests.get(url=url_search_track, params=query, headers=headers)

        try:
            track_uri = response_track.json()["tracks"]["items"][0]["uri"]
        except IndexError:
            print("Track not found, skip over this")
        return track_uri

    def user_id(self, token):

        url_check_user = "https://api.spotify.com/v1/me"
        headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
                  }

        check_user = requests.get(url=url_check_user, headers=headers)
        print(check_user.status_code)
        user_id = check_user.json()["id"]
        return user_id

    def create_playlist(self, name, description, token):

        user_id = self.user_id(self.acces_token)
        url_playlist = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        playlist_data = {
            "name": name,
            "description": description,
            "public": "false"
        }

        create_playlist = requests.post(url=url_playlist, json=playlist_data, headers=headers)
        print(create_playlist.status_code)
        playlist_id = create_playlist.json()["id"]
        print(playlist_id)
        return playlist_id

    def add_tracks_to_playlist(self, uri_list, playlist_id, token):

        url_compose_playlist = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        data_compose_playlist = {"uris": uri_list}

        compose_playlist = requests.post(url=url_compose_playlist, json=data_compose_playlist, headers=headers)
        print(compose_playlist.status_code)



