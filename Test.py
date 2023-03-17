import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

import json

# Variables for authentication
username = 'your_username'
client_id= os.getenv("Client_id")
client_secret= os.getenv("Client_secret")
redirect_uri = os.getenv("REDIRECT") 
user= os.getenv("USER")

Scope = 'playlist-modify-public'
spotifyOBJ = SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = Scope, username = user)
spotify = spotipy.Spotify(auth_manager = spotifyOBJ)

playlistName = input("Name of playlist")
playlistDesc = input("Description of playlist")

spotify.user_playlist_create(user = user, name = playlistName, public = True, description = playlistDesc)

song = input('Enter Song')

search = spotify.search(q = song)

songs = []

songs.append(search['tracks']['items'][0]['uri'])

playlists = spotify.user_playlists(user = user)
newPlaylist = playlists['items'][0]['id']

spotify.user_playlist_add_tracks(user = user,playlist_id = newPlaylist,tracks = songs)
