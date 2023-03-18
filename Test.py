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

#initial setup
Scope = 'playlist-modify-public'
spotifyOBJ = SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = Scope, username = user)
spotify = spotipy.Spotify(auth_manager = spotifyOBJ)

#inputs
genresJSON = spotify.recommendation_genre_seeds()
genres = genresJSON['genres']


for i in range(len(genres)):
    index = i + 1
    print(index,". " , genres[i])

targetGenre = input("Please select # to explore genre: ")
targetGenre = int(targetGenre) - 1
numTracks = input("Number of tracks: ")
numTracks = int(numTracks)


recommendations = spotify.recommendations(seed_genres = [genres[targetGenre]] , limit = numTracks)

#playlist create
playlistName = genres[targetGenre] + " exploration"
playlistDesc = "Playlist of all " + genres[targetGenre] + " songs."

spotify.user_playlist_create(user = user, name = playlistName, public = True, description = playlistDesc)

#grab newPlaylist as newest playlist created
playlists = spotify.user_playlists(user = user)
newPlaylist = playlists['items'][0]['id']

print(newPlaylist)

tracklist = []
for i in range(numTracks):
    tracklist.append(recommendations['tracks'][i]['uri'])

print(tracklist)
    
