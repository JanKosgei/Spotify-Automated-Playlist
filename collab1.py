import spotipy
import spotipy.util as util
import os
from dotenv import load_dotenv
import base64
from requests import post


# Variables for authentication
username = 'your_username'
client_id= os.getenv("Client_id")
client_secret= os.getenv("Client_secret")
redirect_uri = "https://accounts.spotify.com/api/token"
# Authentication
def get_token():
    auth_string =str(client_id)  + ":" + str(client_secret)
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization":
               "Basic " + auth_base64,
               "Content-type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = result.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()

# Create Spotify object
spotify = spotipy.Spotify(auth=token)

# Get user input
genre = input('Please enter a genre: ')
artist = input('Please enter an artist: ')
mood = input('Please enter a mood: ')

# Search for songs using the API
query = 'genre:{} artist:{} mood:{}'.format(genre, artist, mood)
results = spotify.search(query, type='track')

# Print out the results
print(results)

# Select songs for the playlist
song_list = []
for result in results['tracks']['items']:
    # Get the song's popularity and release date
    popularity = result['popularity']
    release_date = result['album']['release_date']

    # Get the song's tempo
    audio_features = spotify.audio_features(result['id'])
    tempo = audio_features[0]['tempo']

    # Use algorithm to select the song
    if popularity > 70 and release_date > '2010-01-01' and tempo > 120:
        song_list.append(result['id'])

# Print out the list of songs
print(song_list)

# Create playlist
playlist_name = 'My Automated Playlist'
playlist = spotify.user_playlist_create(username, playlist_name)

# Print out the playlist information
print(playlist)

# Add songs to playlist
playlist_id = playlist['id']
spotify.user_playlist_add_tracks(username, playlist_id, song_list)

# Error handling and testing
try:
    # Make sure the playlist was created properly
    playlist = spotify.user_playlist(username, playlist_id)
    if playlist['name'] == playlist_name:
        print('Playlist created successfully!')
    else:
        print('Error creating playlist.')

except spotipy.SpotifyException as e:
    # Handle spotify API errors
    print('Error creating playlist: {}'.format(e))