import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


titleScreen = """
====================================
    SPOTIFY NEW MUSIC EXPLORER:
        create playlsts with
        undiscovered music !
====================================
"""
# Variables for authentication
username = 'your_username'
client_id= os.getenv("Client_id")
client_secret= os.getenv("Client_secret")
redirect_uri = os.getenv("REDIRECT") 
user= os.getenv("USER")

#initial setup for spotify object
Scope = 'playlist-modify-public'
spotifyOBJ = SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = Scope, username = user)
spotify = spotipy.Spotify(auth_manager = spotifyOBJ)
genresJSON = spotify.recommendation_genre_seeds()
genres = genresJSON['genres']

    
class PlaylistGenerator:


    def __init__(self):
        #initialize values
        self.targetGenre = 0
        self.numTracks = 0
        self.recommendations = []
        self.newPlaylist = ''
        self.tracklist = []
        
    def getInputs(self):
        #get data about playlist to generate
        self.targetGenre = input("Please select # to explore genre: ")
        self.targetGenre = int(self.targetGenre) - 1
        self.numTracks = int(input("Number of tracks within playlist(1 - 100): "))
        self.numTracks = int(self.numTracks)

    def showGenres(self):
        for n in range(len(genres)):
            index = n + 1
            print(index,". " , genres[n])

    def getRecommendations(self):
        #generates number of recommended tracks
        print(self.targetGenre)
        self.recommendations = spotify.recommendations(seed_genres = [genres[self.targetGenre], genres[self.targetGenre + 1]] , limit = self.numTracks)

    def makePlaylist(self):
        #makes new playlist
        playlistName = genres[self.targetGenre] + " exploration"
        playlistDesc = "Playlist of undiscovered " + genres[self.targetGenre] + " songs."

        spotify.user_playlist_create(user = user, name = playlistName, public = True, description = playlistDesc)
        playlists = spotify.user_playlists(user = user)
        self.newPlaylist = playlists['items'][0]['id']

    def addTracks(self):
        for i in range(self.numTracks):
            self.tracklist.append(self.recommendations['tracks'][i]['uri'])

        spotify.user_playlist_add_tracks(user = user, playlist_id = self.newPlaylist, tracks = self.tracklist)

    def reset(self):
        self.targetGenre = 0
        self.numTracks = 0
        self.recommendations = []
        self.newPlaylist = ''
        self.tracklist = []
            
def main():
    generator = PlaylistGenerator()
    input(titleScreen)
    os.system('cls')
    
    while True:
        generator.showGenres()
        generator.getInputs()
        generator.getRecommendations()
        generator.makePlaylist()
        generator.addTracks()
        generator.reset()

if __name__ == "__main__":
    main()