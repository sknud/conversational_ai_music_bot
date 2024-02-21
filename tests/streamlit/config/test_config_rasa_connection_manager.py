from unittest.mock import patch, mock_open
import pytest
import json
from src.streamlit.config.config_rasa_connection_manager import load_rasa_endpoint

def test_load_rasa_endpoint_local_success():
    mock_data = json.dumps({"url_local": "http://localhost:5005", "url_aws": "http://aws-host:5005"})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        endpoint = load_rasa_endpoint("config.json")
        assert endpoint == "http://localhost:5005"

def test_load_rasa_endpoint_aws_success():
    mock_data = json.dumps({"url_local": "http://localhost:5005", "url_aws": "http://aws-host:5005"})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        endpoint = load_rasa_endpoint("config.json", use_local=False)
        assert endpoint == "http://aws-host:5005"

def test_load_rasa_endpoint_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        endpoint = load_rasa_endpoint("nonexistent.json")
        assert endpoint is None

def test_load_rasa_endpoint_missing_key():
    mock_data = json.dumps({"url_local": "http://localhost:5005"})  # Missing 'url_aws'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        endpoint = load_rasa_endpoint("config.json", use_local=False)
        assert endpoint is None

def test_load_rasa_endpoint_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        endpoint = load_rasa_endpoint("config.json")
        assert endpoint is None

