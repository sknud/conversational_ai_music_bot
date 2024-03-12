import streamlit as st
from utils.id_generator import generate_device_id, generate_session_id
from rasa_communication.rasa_handler import manage_chat_session
from config.config_rasa_connection_manager import load_rasa_endpoint

def run_chat_interface():
    st.title("💬 Music Chatbot")
    st.caption("🚀 A chatbot powered by RASA (backend) and Streamlit (frontend)")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    device_id = generate_device_id()
    session_id = generate_session_id()
    config_file_path = 'src/streamlit/config.yml'
    rasa_endpoint = load_rasa_endpoint(config_file_path)
    manage_chat_session(device_id, session_id, rasa_endpoint)
