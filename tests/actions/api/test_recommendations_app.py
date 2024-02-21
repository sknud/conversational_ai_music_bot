from unittest.mock import patch
import pytest
from src.actions.api.recommendations_app import get_recommendations 

@pytest.fixture
def spotify_track_search_mock():
    return {
        "tracks": {
            "items": [
                {
                    "uri": "spotify:track:12345",
                    "name": "Test Track",
                    "artists": [{"name": "Test Artist"}]
                }
            ]
        }
    }

@pytest.fixture
def spotify_artist_search_mock():
    return {
        "artists": {
            "items": [
                {
                    "uri": "spotify:artist:67890"
                }
            ]
        }
    }

@pytest.fixture
def spotify_recommendations_mock():
    return {
        "tracks": [
            {
                "name": "Recommended Track 1",
                "artists": [{"name": "Artist 1"}],
                "uri": "spotify:track:11111"
            },
            {
                "name": "Recommended Track 2",
                "artists": [{"name": "Artist 2"}],
                "uri": "spotify:track:22222"
            }
        ]
    }

@patch('spotipy.Spotify.search')
@patch('spotipy.Spotify.recommendations')
def test_get_recommendations_by_track(mock_recommendations, mock_search, spotify_track_search_mock, spotify_recommendations_mock):
    mock_search.return_value = spotify_track_search_mock
    mock_recommendations.return_value = spotify_recommendations_mock
    recommendations = get_recommendations(song_title="Test Track")
    assert len(recommendations) == 2
    assert recommendations[0]['name'] == "Recommended Track 1"
    assert recommendations[1]['name'] == "Recommended Track 2"

@patch('spotipy.Spotify.search')
@patch('spotipy.Spotify.recommendations')
def test_get_recommendations_by_artist(mock_recommendations, mock_search, spotify_artist_search_mock, spotify_recommendations_mock):
    mock_search.return_value = spotify_artist_search_mock
    mock_recommendations.return_value = spotify_recommendations_mock
    recommendations = get_recommendations(artist="Test Artist")
    assert len(recommendations) == 2
    assert recommendations[0]['artist'] == "Artist 1"
    assert recommendations[1]['artist'] == "Artist 2"

@patch('spotipy.Spotify.search')
def test_get_recommendations_no_results(mock_search):
    mock_search.return_value = {"tracks": {"items": []}, "artists": {"items": []}}
    recommendations = get_recommendations(song_title="Nonexistent Track", artist="Nonexistent Artist")
    assert recommendations is None
