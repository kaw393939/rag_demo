import os
import streamlit as st
import yaml
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize OpenAI client
    if "openai_client" not in st.session_state:
        try:
            # Attempt to create OpenAI client
            st.session_state.openai_client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        except Exception as e:
            st.error(f"Failed to initialize OpenAI client: {e}")
            st.session_state.openai_client = None

def load_configuration():
    """Load configuration from config.yaml with error handling."""
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        st.warning("Config file not found. Using default settings.")
        return {
            "system_prompt": "You are a helpful assistant.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }
    except yaml.YAMLError as e:
        st.error(f"Error parsing config file: {e}")
        return {
            "system_prompt": "You are a helpful assistant.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }

def send_message(user_message):
    """Handle a new message submission and get a response from OpenAI using streaming."""
    # Validate input
    if not user_message:
        return

    # Check if OpenAI client is initialized
    if not hasattr(st.session_state, 'openai_client') or st.session_state.openai_client is None:
        st.error("OpenAI client is not properly initialized. Please check your API key.")
        return

    # Load configuration
    config = load_configuration()

    # Append user's message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    try:
        # Prepare messages for API call
        messages = [
            {"role": "system", "content": config.get("system_prompt", "You are a helpful assistant.")}
        ] + st.session_state.chat_history

        # Generate response with streaming
        response_stream = st.session_state.openai_client.chat.completions.create(
            model=config.get("model", "gpt-3.5-turbo"),
            messages=messages,
            temperature=config.get("temperature", 0.7),
            stream=True
        )

        # Create a placeholder for streaming response
        response_placeholder = st.empty()
        full_response = ""

        # Stream the response
        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response)

        # Add full response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"An error occurred: {e}")

def clear_chat():
    """Clear the chat history."""
    st.session_state.chat_history = []

def main():
    """Main function for the Streamlit chat application."""
    # Set page configuration
    st.set_page_config(page_title="OpenAI Chat Interface", page_icon="💬")

    # Initialize session state
    initialize_session_state()

    # Page title and description
    st.title("🤖 OpenAI Chat Interface")
    st.markdown("Chat with an AI powered by OpenAI's language models.")

    # API Key check
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI API key is missing. Please set it in your .env file.")
        return

    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.chat_message("user").markdown(message['content'])
        else:
            st.chat_message("assistant").markdown(message['content'])

    # Clear chat button
    if st.sidebar.button("🧹 Clear Chat History"):
        clear_chat()

    # User input
    user_input = st.chat_input("Enter your message...")
    if user_input:
        send_message(user_input)

if __name__ == "__main__":
    main()