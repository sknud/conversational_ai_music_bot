import logging

class SingletonLogger:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_logger()
        return cls._instance

    @staticmethod
    def _create_logger():
        logger = logging.getLogger("MusicBotLogger")
        logger.setLevel(logging.INFO)
        # Add any handlers, formatters here
        return logger
