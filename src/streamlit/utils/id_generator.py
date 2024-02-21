import random
import uuid
import logging
from src.streamlit.utils.logger import SingletonLogger

logger = SingletonLogger.get_instance()

def generate_session_id():
    session_id = random.randint(1, 1000000)
    logger.info("session ID: %s", session_id)
    return session_id


def generate_device_id():
    machine_id = str(uuid.getnode())
    logger.info("machine ID: %s", machine_id)
    return machine_id