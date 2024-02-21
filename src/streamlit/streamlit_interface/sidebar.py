# sidebar.py
import streamlit as st

def setup_sidebar():
    with st.sidebar:
        st.write("EXPLANATION OF HOW TO USE THE APP")
        st.write("Starting a Conversation:")
        st.write("-Simply type your question or message in the chat window.")
        st.write("If you're visiting for the first time, our chatbot might start with a greeting and ask a couple of questions to understand your needs better.")
        st.write("Asking Questions:")
        st.write("Be clear and specific with your questions.")
        st.write("Our chatbot is designed to understand natural language, so feel free to ask questions to do with music as you would in a normal conversation.")
        st.write("For example you can ask it music recommendation questions or music trivia questions. For specific examples see the Github page.")
        st.write("PRIVACY POLICY")
        st.write("By using this application you agree to its privacy policy")
        # Link or button to navigate to the Privacy Policy page
        if st.button("Privacy Policy"):
            st.session_state["current_page"] = "privacy_policy"


