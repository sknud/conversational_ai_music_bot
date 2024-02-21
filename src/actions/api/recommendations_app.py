import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_recommendations(song_title=None, artist=None, limit=5):
    try:
        seed_tracks = []
        seed_artists = []

        if song_title:
            # Search for the track and get its URI
            track_results = sp.search(q=song_title, type='track', limit=1)
            if track_results['tracks']['items']:
                seed_tracks = [track_results['tracks']['items'][0]['uri']]

        if artist and not seed_tracks:  # Prioritize song title if available
            # Search for the artist and get their URI
            artist_results = sp.search(q=artist, type='artist', limit=1)
            if artist_results['artists']['items']:
                seed_artists = [artist_results['artists']['items'][0]['uri']]

        if not seed_tracks and not seed_artists:
            return None  # No results for either the track or the artist

        # Get recommended tracks based on the seed tracks or artists
        recommendations = sp.recommendations(seed_tracks=seed_tracks, seed_artists=seed_artists, limit=limit)['tracks']
        return [{'name': track['name'], 'artist': track['artists'][0]['name'], 'uri': track['uri']} for track in recommendations]

    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return None
