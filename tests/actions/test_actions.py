from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
import pytest
from src.actions.actions import ActionMusicRecommendation, ActionTriviaReleaseDate, ActionTriviaArtistBiography, ActionTriviaAlbumTrackList
import os
from unittest.mock import Mock, patch, MagicMock


### Music Recommendation Action Tests ###

@pytest.mark.asyncio
async def test_action_music_recommendation_with_song_title(monkeypatch):
    '''
    In this test a song title is provided, so the message 'Mock recommendation response.' should be returned
    '''
    # Use monkeypatch to set the environment variable for test mode
    monkeypatch.setenv("RASA_TEST_MODE", "True")

    # Create dispatcher and tracker with relevant slots/entities
    dispatcher = CollectingDispatcher()
    tracker = Tracker(
        "default",
        slots={"song_title": "Imagine"},
        latest_message={"entities": [{"entity": "song_title", "value": "Imagine"}]},
        events=[],
        paused=False,
        followup_action=None,
        active_loop=None,
        latest_action_name=None
    )

    # Create instance of the action
    action = ActionMusicRecommendation()

    # Run the action
    events = action.run(dispatcher, tracker, {})

    # Check the response
    messages = dispatcher.messages
    assert len(messages) == 1
    assert "Mock recommendation response." in messages[0]['text']


@pytest.mark.asyncio
async def test_action_music_recommendation_without_song_title(monkeypatch):
    '''
    In this test no song title is provided, so the message 'Please specify a song or an artist to get recommendations.' should be returned
    '''
    # Use monkeypatch to set the environment variable for test mode
    monkeypatch.setenv("RASA_TEST_MODE", "True")

    # Create dispatcher and tracker without song title entity
    dispatcher = CollectingDispatcher()
    tracker = Tracker(
        "default",
        slots={},  # No song title slot
        latest_message={"entities": []},  # No entities in the latest message
        events=[],
        paused=False,
        followup_action=None,
        active_loop=None,
        latest_action_name=None
    )

    # Create instance of the action
    action = ActionMusicRecommendation()

    # Run the action
    events = action.run(dispatcher, tracker, {})

    # Check the response (should ask the user to specify a song or an artist)
    messages = dispatcher.messages
    assert len(messages) == 1
    assert messages[0]['text'] == "Please specify a song or an artist to get recommendations."


### Trivia Release Date Action Tests ###

@pytest.mark.asyncio
async def test_action_trivia_release_date_with_album_title(monkeypatch):
    '''
    In this test an album title is provided, so the message 'The album 'Abbey Road' was released on...' should be returned
    '''
    # Use monkeypatch to set the environment variable for test mode
    monkeypatch.setenv("RASA_TEST_MODE", "True")

    # Create dispatcher and tracker with an album title entity
    dispatcher = CollectingDispatcher()
    tracker = Tracker(
        "default",
        slots={},
        latest_message={"entities": [{"entity": "album_title", "value": "Abbey Road"}]},
        events=[],
        paused=False,
        followup_action=None,
        active_loop=None,
        latest_action_name=None
    )

    # Create instance of the action
    action = ActionTriviaReleaseDate()

    # Run the action
    events = action.run(dispatcher, tracker, {})

    # Check the response for the provided album title
    messages = dispatcher.messages
    assert len(messages) == 1
    assert "The album 'Abbey Road' was released on" in messages[0]['text']

@pytest.mark.asyncio
async def test_action_trivia_release_date_without_album_title(monkeypatch):
    '''
    In this test no album title is provided, so the message 'Please specify an album to get its release date.' should be returned
    '''
    # Use monkeypatch to set the environment variable for test mode
    monkeypatch.setenv("RASA_TEST_MODE", "True")

    # Create dispatcher and tracker without an album title entity
    dispatcher = CollectingDispatcher()
    tracker = Tracker(
        "default",
        slots={},
        latest_message={"entities": []},
        events=[],
        paused=False,
        followup_action=None,
        active_loop=None,
        latest_action_name=None
    )

    # Create instance of the action
    action = ActionTriviaReleaseDate()

    # Run the action
    events = action.run(dispatcher, tracker, {})

    # Check the response when no album title is provided
    messages = dispatcher.messages
    assert len(messages) == 1
    assert "Please specify an album to get its release date." in messages[0]['text']


### Trivia Artist Biography Action Tests ###

@pytest.mark.asyncio
async def test_action_artist_biography_with_artist_name(monkeypatch):
    """
    In this test an artist name is provided, so the message 'Sample biography for artist.' should be returned
    """
    # Use monkeypatch to set the environment variable for test mode
    os.environ["RASA_TEST_MODE"] = "True"

    # Create dispatcher and tracker with artist entity
    dispatcher = CollectingDispatcher()
    tracker = Tracker(
        "default",
        slots={},
        latest_message={"entities": [{"entity": "artist", "value": "The Beatles"}]},
        events=[],
        paused=False,
        followup_action=None,
        active_loop=None,
        latest_action_name=None
    )

    # Create instance of the action
    action = ActionTriviaArtistBiography()

    # Run the action
    events = action.run(dispatcher, tracker, {})

    # Check the response
    messages = dispatcher.messages
    assert len(messages) == 1
    assert "Sample biography for artist." in messages[0]['text']
    

@pytest.mark.asyncio
async def test_action_artist_biography_without_artist_name(monkeypatch):
    """
    In this test, no artist is provided, so the message 'No artist name provided.' should be returned
    """
    # Use monkeypatch to set the environment variable for test mode
    os.environ["RASA_TEST_MODE"] = "True"

    # Create dispatcher and tracker without artist entity
    dispatcher = CollectingDispatcher()
    tracker = Tracker(
        "default",
        slots={},
        latest_message={"entities": []},
        events=[],
        paused=False,
        followup_action=None,
        active_loop=None,
        latest_action_name=None
    )

    # Create instance of the action
    action = ActionTriviaArtistBiography()

    # Run the action
    events = action.run(dispatcher, tracker, {})

    # Check the response (should be an empty message or a specific message for no artist provided)
    messages = dispatcher.messages
    assert len(messages) == 1
    assert messages[0]['text'] == "No artist name provided." 

## Trivia Album Tracklist Action Tests ###

@pytest.mark.asyncio
@patch('src.actions.actions.get_album_tracklist')
async def test_action_trivia_album_tracklist_with_album(mock_get_album_tracklist):
    # Set up the mock to return a specific value
    mock_get_album_tracklist.return_value = ['Song 1', 'Song 2', 'Song 3']

    # Create a mock Tracker
    tracker = Tracker("default", {}, {}, [], False, None, {}, "action_listen")
    tracker.slots['album_title'] = 'Thriller'

    # Create a mock Dispatcher
    dispatcher = CollectingDispatcher()

    # Create an instance of your custom action
    action = ActionTriviaAlbumTrackList()

    # Call the run method
    await action.run(dispatcher, tracker, {})

    # Get the messages sent by the dispatcher
    messages = dispatcher.messages

    # Assert that the result is as expected
    expected_message = "The tracks in 'Thriller' are: Song 1, Song 2, Song 3"
    assert len(messages) > 0  # Ensure there is at least one message
    assert messages[0]['text'] == expected_message

@pytest.mark.asyncio
@patch('src.actions.actions.get_album_tracklist')
async def test_action_trivia_album_tracklist_no_album_title(mock_get_album_tracklist):
    # No need to set up the mock since it shouldn't be called

    # Create a mock Tracker with no album_title slot set
    tracker = Tracker("default", {}, {}, [], False, None, {}, "action_listen")

    # Create a mock Dispatcher
    dispatcher = CollectingDispatcher()

    # Create an instance of your custom action
    action = ActionTriviaAlbumTrackList()

    # Call the run method
    await action.run(dispatcher, tracker, {})

    # Get the messages sent by the dispatcher
    messages = dispatcher.messages

    # Assert that the bot responded with a message for no album title
    expected_message = "I couldn't recognise an album name in your message. You might have to ask about a more popular album!"
    assert len(messages) > 0
    assert messages[0]['text'] == expected_message


@pytest.fixture
async def mock_get_album_tracklist():
    with patch('src.actions.api.music_trivia_app.get_album_tracklist') as mock_func:
        yield mock_func


@pytest.mark.asyncio
@patch('src.actions.api.music_trivia_app.get_album_tracklist')
async def test_action_trivia_album_tracklist_no_tracks_with_album_title_without_artist(mock_get_album_tracklist):
    # Set up the mock to return None or an empty list
    mock_get_album_tracklist.return_value = None

    # Create a mock Tracker with album_title slot set
    tracker = Tracker("default", {}, {}, [], False, None, {}, "action_listen")
    tracker.slots['album_title'] = 'sljndljkn' #fake album name

    # Create a mock Dispatcher
    dispatcher = CollectingDispatcher()

    # Create an instance of your custom action
    action = ActionTriviaAlbumTrackList()

    # Call the run method
    await action.run(dispatcher, tracker, {})

    # Get the messages sent by the dispatcher
    messages = dispatcher.messages

    # Assert that the bot responded with a message for no tracks found
    expected_message = "I couldn't find the tracklist for that album, apologies!"
    assert len(messages) > 0
    assert messages[0]['text'] == expected_message

@pytest.mark.asyncio
# async def test_action_trivia_album_tracklist_no_tracks_with_album_title_with_artist(mock_get_album_tracklist):
#     # Set up the mock to return None or an empty list
#     mock_get_album_tracklist.return_value = None

async def test_action_trivia_album_tracklist_no_tracks_with_album_title_with_artist():
    mock_get_album_tracklist = MagicMock()
    mock_get_album_tracklist.__aiter__.return_value = iter([])  # Mock the asynchronous iterator

    # Create a mock Tracker with album_title and artist slots set
    tracker = Tracker("default", {}, {}, [], False, None, {}, "action_listen")
    tracker.slots['album_title'] = 'sljndljkn' #fake album name
    tracker.slots['artist'] = 'kjbskjnbdns' #fake artist name

    # Create a mock Dispatcher
    dispatcher = CollectingDispatcher()

    # Create an instance of your custom action
    action = ActionTriviaAlbumTrackList()

    # Call the run method
    await action.run(dispatcher, tracker, {})

    # Get the messages sent by the dispatcher
    messages = dispatcher.messages

    # Assert that the bot responded with a message for no tracks found even with artist name
    expected_message = "I couldn't find the album 'sljndljkn' by kjbskjnbdns."
    assert len(messages) > 0
    assert messages[0]['text'] == expected_message










