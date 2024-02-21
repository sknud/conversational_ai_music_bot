from streamlit_interface.sidebar import setup_sidebar
from streamlit_interface.chat_interface import run_chat_interface
from streamlit_interface.privacy_policy import show_privacy_policy
import streamlit as st

# Import show_privacy_policy if it's defined in another module
from streamlit_interface.privacy_policy import show_privacy_policy

def main():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    setup_sidebar()

    # Display the appropriate page based on the current_page value
    if st.session_state["current_page"] == "privacy_policy":
        show_privacy_policy()
    else:
        run_chat_interface()

if __name__ == "__main__":
    main()
