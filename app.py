import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

# Replace this with your actual n8n webhook URL (No Auth)
INPUT_WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Sends user message & returns AI response
BOT_NAME = os.getenv("BOT_NAME", "CHATBOT") 

def generate_session_id():
    """Generate a unique session ID for each user"""
    return str(uuid.uuid4())

def send_message_to_n8n(session_id, message):
    """Send user message to n8n's webhook and return AI response"""
    payload = {"sessionId": session_id, "chatInput": message}
    try:
        response = requests.post(INPUT_WEBHOOK_URL, json=payload, timeout=300)
        if response.status_code == 200:
            json_response = response.json()
            
            return json_response.get("output", "🤖 No AI response received.")  # Extract response
        else:
            return f"⚠️ Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Connection Error: {str(e)}"

def main():
    st.title(f"{BOT_NAME}")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Send message to n8n and retrieve response
        llm_response = send_message_to_n8n(st.session_state.session_id, user_input)

        # Display assistant message
        st.session_state.messages.append({"role": "assistant", "content": llm_response})
        with st.chat_message("assistant"):
            st.write(llm_response)

if __name__ == "__main__":
    main()
