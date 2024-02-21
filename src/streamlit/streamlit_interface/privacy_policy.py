import streamlit as st

def show_privacy_policy():

    # Button to return to the main chatbot
    if st.button("Back to Chat", key="privacy_policy_back_top_of_page"):
        st.session_state["current_page"] = "home"
        st.rerun()

    st.title("Privacy Policy")
    st.write("""
    Privacy Policy

Last Updated: 19.01.2024

Introduction

We are committed to protecting your personal information and your right to privacy. This Privacy Policy explains what information we collect, how we use it, and what rights you have in relation to it.

Information Collection and Use

We collect minimal personal information required for the operation of this chatbot. This may include:

    Input Data: Any text or voice input provided by you during your interaction with the chatbot.
    Usage Data: Information such as how often you interact with the chatbot and response times.

How We Use Your Information

We use the information we collect to:

    Provide, operate, and maintain our chatbot services.
    Improve, personalize, and expand our chatbot services.
    Understand and analyze how you use our chatbot.
    Develop new products, services, features, and functionality.

Data Sharing and Disclosure

We do not share or disclose any personal information collected through our chatbot except as described in this policy. We may disclose information:

    To comply with any applicable law or regulation.
    To protect the rights, property, or safety of our users or others.

Data Retention

We retain collected information for as long as necessary to provide you with your requested service. Once the retention period expires, we delete or anonymize your information.

Your Privacy Rights

You have the right to:

    Access, update, or delete the information we have on you.
    Request that we stop using or collecting your personal information.

Changes to This Privacy Policy

We reserve the right to modify this privacy policy at any time, so please review it frequently. Changes and clarifications will take effect immediately upon their posting on the website.

    """)
    # Button to return to the main chatbot
    if st.button("Back to Chat", key="privacy_policy_back_bottom_of_page"):
        st.session_state["current_page"] = "home"
        st.rerun()