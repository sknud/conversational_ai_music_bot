from src.streamlit.rasa_communication.rasa_handler import send_request_to_rasa, process_rasa_response, manage_chat_session
from unittest.mock import patch, MagicMock
import pytest
import json
from src.streamlit.utils.logger import SingletonLogger

@patch('src.streamlit.rasa_communication.rasa_handler.requests.post')
@patch('src.streamlit.rasa_communication.rasa_handler.logger')
@patch('src.streamlit.rasa_communication.rasa_handler.process_rasa_response', return_value="Processed Response")
@patch('src.streamlit.rasa_communication.rasa_handler.st')
def test_send_request_to_rasa_success(mock_st, mock_process_rasa_response, mock_logger, mock_post):
    # Setup mock for requests.post to return a successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = json.dumps({"reply": "Test response from Rasa"})
    mock_post.return_value = mock_response

    # Call the function under test
    response_message = send_request_to_rasa("test_sender", "test_message", "http://test_rasa_endpoint")

    # Assertions
    mock_post.assert_called_once_with("http://test_rasa_endpoint", json={"sender": "test_sender", "message": "test_message"}, headers={"Content-Type": "application/json"}, timeout=20)
    mock_logger.info.assert_called()  # Check if logger.info was called, you can also check the exact call parameters
    mock_process_rasa_response.assert_called_once_with({"reply": "Test response from Rasa"})
    assert response_message == "Processed Response"
    mock_st.error.assert_not_called()  # Ensure st.error was not called since this is a successful request

def test_send_request_to_rasa_invalid_endpoint():
    with pytest.raises(ValueError):
        send_request_to_rasa("sender", "message", None)

def test_process_rasa_response_valid_response():
    response_json = [{"text": "Test response"}]
    bot_message = process_rasa_response(response_json)
    assert bot_message == "Test response"

def test_process_rasa_response_empty_response():
    response_json = []
    bot_message = process_rasa_response(response_json)
    assert bot_message == "I'm not sure how to respond to that."

def test_process_rasa_response_missing_text_field():
    response_json = [{"other_field": "value"}]
    bot_message = process_rasa_response(response_json)
    assert bot_message == "I'm not sure how to respond to that."

@patch('src.streamlit.rasa_communication.rasa_handler.st')
def test_manage_chat_session_success(mock_st):
    # Mock user input through st.chat_input
    mock_st.chat_input.return_value = "User message"

    # Mock session state to have a messages list
    mock_st.session_state.messages = []

    # Mock the empty container for the bot's response
    response_placeholder = MagicMock()
    mock_st.empty.return_value = response_placeholder

    # Mock send_request_to_rasa to return a specific message
    with patch('src.streamlit.rasa_communication.rasa_handler.send_request_to_rasa', return_value="Bot response") as mock_send_request:
        manage_chat_session("device_id_123", "session_id_123", "http://rasa_endpoint")

        # Verify send_request_to_rasa was called with the correct arguments
        mock_send_request.assert_called_once_with("session_id_123", "User message", "http://rasa_endpoint")

        # Check if the user's message was added to session state
        assert mock_st.session_state.messages[0] == {"role": "user", "content": "User message"}

        # Check if the bot's message was added to session state
        assert mock_st.session_state.messages[1] == {"role": "assistant", "content": "Bot response"}

        # Verify the response placeholder was updated with the bot's message
        response_placeholder.markdown.assert_called_once_with("Bot response")

@patch('src.streamlit.rasa_communication.rasa_handler.st')
def test_manage_chat_session_no_input(mock_st):
    # Simulate no user input
    mock_st.chat_input.return_value = None

    # Mock session state to have a messages list
    mock_st.session_state.messages = []

    with patch('src.streamlit.rasa_communication.rasa_handler.send_request_to_rasa') as mock_send_request:
        manage_chat_session("device_id_123", "session_id_123", "http://rasa_endpoint")

        # Ensure send_request_to_rasa was not called since there's no input
        mock_send_request.assert_not_called()

        # Verify no messages were added to session state
        assert len(mock_st.session_state.messages) == 0