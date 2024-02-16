import requests
import html
import lxml
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

year = input("Type in YYYY-MM-DD format.\n")

request = requests.get(f"https://www.billboard.com/charts/hot-100/{year}")
data = request.text

soup = BeautifulSoup(data, "html.parser")
songs = soup.findAll("h3", class_="c-title")
song_list = []

for n in range(7,len(songs),4):
    song = songs[n].getText().strip()
    song_list.append(song)

updated_list = song_list[0:100]
# print(updated_list)

#---------------- Spotfy Login -------------#

id = "your id"
secret = "your password"

spotfy = SpotifyOAuth(client_id=id,
                        client_secret=secret,
                        scope = "playlist-modify-private",
                        redirect_uri = "http://localhost:8888/callback",
                        show_dialog=True,
                        cache_path="token.txt"
                        )

sp = spotipy.Spotify(auth_manager=spotfy)

user_id = sp.current_user()["id"]
print(user_id)

#------------------ Procurar Musicas -----------------#
song_links = []
for item in updated_list:

    result = sp.search(q=f"track:{item} year:{year.split('-')[0]}",type="track")
    try:
        link = result["tracks"]["items"][0]["uri"]
        print(link)
        song_links.append(link)
    except IndexError:
        print("Song not found.")

#------------------ Creating a Playlist ---------------#

playlist = sp.user_playlist_create(user=user_id,name=f"{year} Billboard Top 100",
                                   public=False,description="Playlist created in Python.")

sp.playlist_add_items(playlist_id=playlist["id"],items=song_links[0:100])


