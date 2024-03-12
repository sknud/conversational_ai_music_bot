import re
import logging
import json
import requests
from utils.logger import SingletonLogger
import streamlit as st

# from src.streamlit.utils.logger import SingletonLogger

logger = SingletonLogger.get_instance()

# Defining send_request_to_rasa
def send_request_to_rasa(sender, message, rasa_endpoint):
    if rasa_endpoint is None:
        raise ValueError(
            "rasa_endpoint is not initialized. Please call load_rasa_endpoint() first."
        )

    url = rasa_endpoint
    payload = {"sender": sender, "message": message}
    headers = {"Content-Type": "application/json"}
    timeout = 20
    response_message = "Something went wrong connecting to the server. Please try again in 10 seconds."
    try:
        rasa_response = requests.post(url, json=payload, headers=headers, timeout=timeout)
        if rasa_response.status_code == 200:
            logger.info("Request sent successfully")

            if rasa_response.text:
                try:
                    response_json = json.loads(rasa_response.text)
                    logger.info(json.dumps(response_json, indent=4))
                    response_message = process_rasa_response(response_json)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON response received from server.")
                    response_message = "Invalid response format received from server."
            else:
                logger.error("Empty response received from server.")
                response_message = "No response received from server."

        else:
            st.error("Request failed")
            logger.error("Failed response from server with status code: %s", rasa_response.status_code)

    except requests.exceptions.RequestException as e:
        st.error("Request failed")
        st.write("Error:")
        st.write(e)
        logger.error("Error in sending request: %s", e)

    return response_message


def process_rasa_response(response_json):
    if len(response_json) > 0 and "text" in response_json[0]:
        # Extracting the message text
        bot_message = response_json[0]["text"]
        return bot_message
    else:
        # Default message or handling if the expected fields are not present
        return "I'm not sure how to respond to that."


def manage_chat_session(device_id, session_id, rasa_endpoint):
    # Initialize bot_message with a default value
    bot_message = "Error: Failed to get response from Rasa."

    # Check if a message has been sent by the user
    if prompt := st.chat_input("Enter your message: "):

        # Append user's message to session state for display
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Create a placeholder for the chatbot's response
        response_placeholder = st.empty()

        # Display a loading spinner while processing the response
        with st.spinner('Processing...'):
            # Send the user's message to Rasa and get the reply
            try:
                # Send request to Rasa and get the response
                bot_message = send_request_to_rasa(session_id, prompt, rasa_endpoint)

                # Code for debugging in the terminal
                print("Raw bot_message:", bot_message)  # Print the raw response

            # except Exception as e:
            #     st.error(f"An error occurred: {e}")

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to Rasa server: {e}")
                logger.error("Failed to connect to Rasa server: %s", e)

            except ValueError as ve:
                st.error(f"Failed to get response from Rasa: {ve}")
                logger.error("Failed to get response from Rasa: %s", ve)

            except Exception as ex:
                st.error(f"An unexpected error occurred: {ex}")
                logger.error("An unexpected error occurred: %s", ex)

        # Append bot's message to session state for display
        st.session_state.messages.append({"role": "assistant", "content": bot_message})

        # Update the placeholder with the actual response
        response_placeholder.markdown(bot_message)

        # Force Streamlit to rerun the script, updating the display
        st.rerun()
