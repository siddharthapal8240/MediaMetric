import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "fc56d784-6cf2-495d-860b-a215dd1fead2"
FLOW_ID = "e36e3f8d-eb1c-4f08-9bad-b471d618d86a"
APPLICATION_TOKEN = "AstraCS:odylRtZpXHlWEinbtStydgSL:13a603473167e89f75db99a6d1efdcd432e580b9b050b43c84b53d68f885cb20"
ENDPOINT = ""  # Optional endpoint name
TWEAKS = {
    "ChatInput-OKUQw": {},
    "Prompt-5VXuS": {},
    "ChatOutput-O4GYC": {},
    "AstraDBToolComponent-dfyWW": {},
    "Agent-MsS60": {}
}


# Function to run the flow
def run_flow(message: str, endpoint: str = FLOW_ID, tweaks: dict = TWEAKS) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": tweaks,
    }

    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


# Main function for Streamlit
def main():
    st.title("Social Media Performance Analysis")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Input field for the user
    message = st.text_area(
        "Enter your query:",
        placeholder="How can we assist you today?",
        label_visibility="collapsed",
    )

    # Button to send the query
    if st.button("Generate Insights"):
        if not message.strip():
            st.error("Please enter a message")
            return

        with st.spinner("Running flow..."):
            try:
                # Call the API
                response = run_flow(message=message)

                # Extract the main message (assuming the structure)
                main_message = (
                    response.get("outputs", [{}])[0]  # Get the first item in 'outputs' (default to an empty dict)
                    .get("outputs", [{}])[0]  # Access the first item in the nested 'outputs' list
                    .get("results", {})  # Access the 'results' key (default to an empty dict)
                    .get("message", {})  # Access the 'message' key (default to an empty dict)
                    .get("text", "Message not found")  # Extract the 'text' field
                )

            except requests.exceptions.RequestException as e:
                main_message = f"Request error: {e}"
            except (IndexError, AttributeError, KeyError) as e:
                main_message = f"Parsing error: Unable to retrieve the message - {e}"

            # Append user message and response to chat history
            st.session_state["messages"].append({"user": message, "bot": main_message})

    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state["messages"]:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.divider()  # Adds a divider for better readability


if __name__ == "__main__":
    main()
