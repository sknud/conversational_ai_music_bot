from src.streamlit.utils.id_generator import generate_session_id, generate_device_id

from unittest.mock import patch
import pytest
from src.streamlit.utils.id_generator import generate_session_id, generate_device_id

@patch('src.streamlit.utils.id_generator.random.randint')
@patch('src.streamlit.utils.id_generator.logger.info')
def test_generate_session_id(mock_logger_info, mock_randint):
    # Setup the mock to return a specific session ID
    mock_randint.return_value = 123456
    # Call the function under test
    session_id = generate_session_id()
    # Verify the function returns the mocked session ID value
    assert session_id == 123456
    # Check if logger.info was called with the correct parameters
    mock_logger_info.assert_called_once_with("session ID: %s", 123456)

@patch('src.streamlit.utils.id_generator.uuid.getnode')
@patch('src.streamlit.utils.id_generator.logger.info')
def test_generate_device_id(mock_logger_info, mock_getnode):
    # Setup the mock to return a specific machine ID
    mock_getnode.return_value = 987654321
    # Call the function under test
    device_id = generate_device_id()
    # Verify the function returns the expected mocked value, as a string
    assert device_id == '987654321'
    # Check if logger.info was called with the correct parameters
    mock_logger_info.assert_called_once_with("machine ID: %s", '987654321')
