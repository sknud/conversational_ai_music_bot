from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from src.actions.api.recommendations_app import get_recommendations
from src.actions.api.music_trivia_app import get_album_release_date, get_artist_biography, get_album_tracklist
import os


class ActionMusicRecommendation(Action):
    def name(self) -> Text:
        return "action_music_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        recommendations = None

        song_title = tracker.get_slot("song_title") or next((e.get("value") for e in tracker.latest_message['entities'] if e.get("entity") == "song_title"), None)
        artist = tracker.get_slot("artist") or next((e.get("value") for e in tracker.latest_message['entities'] if e.get("entity") == "artist"), None)

        if os.getenv("RASA_TEST_MODE"):
            if song_title:
                message = "Mock recommendation response."
            else:
                message = "Please specify a song or an artist to get recommendations."
        else:
            # Prioritize song recommendations based on song_title if available
            if song_title:
                recommendations = get_recommendations(song_title=song_title)
            elif artist:
                # If no song_title is provided, get recommendations based on artist
                recommendations = get_recommendations(artist=artist)
            else:
                dispatcher.utter_message(text="Please specify a song or an artist to get recommendations.")
                return []

            message = ""
            if recommendations:
                message = "Here are some songs you might like:\n"
                for track in recommendations:
                    message += f"- {track['name']} by {track['artist']}\n"
            else:
                message = "Sorry, I couldn't find any recommendations."

        dispatcher.utter_message(text=message)
        return []

    
class ActionTriviaReleaseDate(Action):

    def name(self) -> Text:
        return "action_trivia_release_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        album_title = next((e.get("value") for e in tracker.latest_message['entities'] if e.get("entity") == "album_title"), None)

        if os.getenv("RASA_TEST_MODE"):
            message = "Mock release date response."
            if not album_title:
                dispatcher.utter_message(text="Please specify an album to get its release date.")
                return []

            # Fetch the release date
            release_date = get_album_release_date(album_title)

            if release_date:
                message = f"The album '{album_title}' was released on {release_date}."
            else:
                message = "Sorry, I couldn't find the release date for that album."

        dispatcher.utter_message(text=message)

        return []

class ActionTriviaArtistBiography(Action):
    def name(self) -> Text:
        return "action_trivia_artist_biography"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        artist_name = next((e.get("value") for e in tracker.latest_message['entities'] if e.get("entity") == "artist"), None)

        if os.environ.get('RASA_TEST_MODE'):
            # Mocked response for testing
            if artist_name:
                biography = "Sample biography for artist."
            else:
                biography = "No artist name provided."  
        else:
            # Real API call
            biography = get_artist_biography(artist_name)
            if not biography:
                biography = "Sorry, I couldn't find a biography for that artist."

        dispatcher.utter_message(text=biography)
        return []

class ActionTriviaAlbumTrackList(Action):
    def name(self) -> Text:
        return "action_trivia_album_tracklist"
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        album_title = tracker.get_slot("album_title")
        artist_name = tracker.get_slot("artist")

        if album_title:
            # First attempt to find the album with the album title alone
            tracks = get_album_tracklist(album_title)

            if tracks:
                # Join the tracks into a single string separated by commas
                tracks_str = ', '.join(tracks)
                # Found the album with album title
                dispatcher.utter_message(text=f"The tracks in '{album_title}' are: {tracks_str}")
            else:
                # If album title alone is not sufficient
                if artist_name:
                    # Try search again including artist name in the search this time
                    tracks = get_album_tracklist(album_title, artist_name)

                    if tracks:
                        # Join the tracks into a single string separated by commas
                        tracks_str = ', '.join(tracks)
                        # Found the album with when user input artist name
                        dispatcher.utter_message(text=f"The tracks in '{album_title}' by {artist_name} are: {tracks_str}")
                    else:
                        # If no results even with artist name
                        dispatcher.utter_message(text=f"I couldn't find the album '{album_title}' by {artist_name}.")
                else:
                    # Unable to find tracklist with album title - normally due to entity recognition limitations
                    dispatcher.utter_message(text=f"I couldn't find the tracklist for that album, apologies!")
        else:
            # Could not recognise album title in user message - normally due to entity recognition limitations
            dispatcher.utter_message(text="I couldn't recognise an album name in your message. You might have to ask about a more popular album!")
        
        return []



    


    
