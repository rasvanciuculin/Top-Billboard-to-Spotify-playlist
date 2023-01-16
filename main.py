import requests
from bs4 import BeautifulSoup
from auth_spotify import SpotifyAuth


date = input("Which year do you want to travel? Type the date in format YYYY-MM-DD ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/ ")
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
titles = soup.select(".a-no-trucate")
titles_list = [tag.getText().strip() for tag in titles]

spotify = SpotifyAuth()
token = spotify.auth_token()

uri_list = []
for i in range(0, len(titles_list)-1, 2):
        song = titles_list[i]
        artist = titles_list[i+1]
        track_uri = spotify.search_track(song, artist, token)
        uri_list.append(track_uri)

# print(uri_list)
playlist_name = input("What's the name of the playlist? ")
playlist_description = input("What's the description of the playlist? ")

playlist_id = spotify.create_playlist(playlist_name, playlist_description, token)
add_to_playlist = spotify.add_tracks_to_playlist(uri_list, playlist_id, token)
