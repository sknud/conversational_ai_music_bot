from unittest.mock import patch
import pytest
import requests_mock
from src.actions.api.music_trivia_app import get_album_release_date, get_artist_biography

@pytest.fixture
def spotify_album_search_mock():
    return {
        "albums": {
            "items": [
                {
                    "id": "album_id_123",
                    "name": "Test Album"
                }
            ]
        }
    }

@pytest.fixture
def spotify_album_details_mock():
    return {
        "release_date": "2020-01-01"
    }

@patch('spotipy.Spotify.search')
@patch('spotipy.Spotify.album')
def test_get_album_release_date_success(mock_album, mock_search, spotify_album_search_mock, spotify_album_details_mock):
    mock_search.return_value = spotify_album_search_mock
    mock_album.return_value = spotify_album_details_mock
    release_date = get_album_release_date("Test Album")
    assert release_date == "2020-01-01"


@patch('spotipy.Spotify.search')
def test_get_album_release_date_no_album_found(mock_search):
    mock_search.return_value = {"albums": {"items": []}}
    release_date = get_album_release_date("Nonexistent Album")
    assert release_date is None

@pytest.fixture
def lastfm_artist_info_mock():
    return {
        "artist": {
            "bio": {
                "content": "Test Artist Biography"
            }
        }
    }

def test_get_artist_biography_success(lastfm_artist_info_mock):
    with requests_mock.Mocker() as m:
        m.get("http://ws.audioscrobbler.com/2.0/", json=lastfm_artist_info_mock)
        bio = get_artist_biography("Test Artist")
        assert bio == "Test Artist Biography"

def test_get_artist_biography_no_artist_found():
    with requests_mock.Mocker() as m:
        m.get("http://ws.audioscrobbler.com/2.0/", json={"error": 6, "message": "Artist not found"})
        bio = get_artist_biography("Nonexistent Artist")
        assert bio is None

def test_get_artist_biography_api_error():
    with requests_mock.Mocker() as m:
        m.get("http://ws.audioscrobbler.com/2.0/", status_code=500)
        bio = get_artist_biography("Test Artist")
        assert bio is None



