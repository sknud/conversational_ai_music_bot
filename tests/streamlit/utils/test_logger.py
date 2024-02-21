import logging
from src.streamlit.utils.logger import SingletonLogger  # Adjust the import path according to your project structure

def test_singleton_logger_instance():
    logger1 = SingletonLogger.get_instance()
    logger2 = SingletonLogger.get_instance()
    # Verify that both calls return the same logger instance
    assert logger1 is logger2
    # Additionally, check that the logger is an instance of logging.Logger
    assert isinstance(logger1, logging.Logger)

def test_logger_configuration():
    logger = SingletonLogger.get_instance()
    # Verify the logger name is as expected
    assert logger.name == "MusicBotLogger"
    # Verify the logging level is set to INFO
    assert logger.level == logging.INFO