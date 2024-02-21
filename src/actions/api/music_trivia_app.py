import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import requests


# Spotify API set up
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# Last FM API Set up
last_fm_api_key = os.getenv("LAST_FM_API_KEY")

def get_album_release_date(album_name):
    try:
        # Search for the album
        results = sp.search(q=album_name, type='album', limit=1)
        if not results['albums']['items']:
            return None  # No results for the album name

        album_id = results['albums']['items'][0]['id']
        album_details = sp.album(album_id)

        # Extract the release date
        release_date = album_details['release_date']
        return release_date
    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return None
    
def get_artist_biography(artist_name):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": last_fm_api_key,
        "format": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    if 'artist' in data and 'bio' in data['artist'] and 'content' in data['artist']['bio']:
        return data['artist']['bio']['content']

    return None

def get_album_tracklist(album_title, artist_name=None):
    # Search query
    query = album_title
    if artist_name:
        query += f" artist:{artist_name}"

    # Search for the album on Spotify
    results = sp.search(query, type='album', limit=1)
    albums = results['albums']['items']

    if not albums:
        return None  # No album found

    # Assuming the first search result is the desired album
    album_id = albums[0]['id']
    tracks = sp.album_tracks(album_id)

    # Extract track names
    tracklist = [track['name'] for track in tracks['items']]
    return tracklist
    
