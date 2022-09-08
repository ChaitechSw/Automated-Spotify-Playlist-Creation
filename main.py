import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests

SPOTIFY_CLIENT_ID = "3a8eb0e9e8f34be0a4f34212803b71d7"
SPOTIFY_CLIENT_SECRET = "2a698fe828c14f72bee24f805ed2307d"

date = input("Which date do you want to travel to? Type that date in this format YYYY-MM-DD: ")

response1 = requests.get("https://www.billboard.com/charts/hot-100/"+date+"/")
billB = response1.text
soup = BeautifulSoup(billB, "html.parser")
items = soup.find_all(name="h3", class_="a-no-trucate")
song_names = []
for song in items:
    song_name = song.getText().replace("\n","")
    song_n = song_name.replace("\t","")
    song_names.append(song_n)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID ,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
