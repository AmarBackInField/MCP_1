import streamlit as st
import uuid
import time
from agent_langgraph import ChatBot

# Initialize chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatBot(memory_enabled=True)
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.user_id = "main_user"
    st.session_state.message_count = 0

chatbot = st.session_state.chatbot
thread_id = st.session_state.thread_id
user_id = st.session_state.user_id

# UI setup
st.set_page_config(page_title="Enhanced Chatbot", layout="centered")
st.title("🤖Scout Agent")

# Sidebar profile section
with st.sidebar:
    st.header("👤 Your Profile")
    name = st.text_input("Your Name", value="User")
    company = st.text_input("Company Name", value="MyCompany")
    email = st.text_input("Email", value="user@example.com")

    if st.button("Update Profile"):
        chatbot.set_user_context(user_id, {
            "name": name,
            "company": company,
            "email": email
        })
        st.success("✅ Profile updated!")

    if st.button("Clear Chat Memory"):
        chatbot.clear_memory(thread_id)
        st.session_state.message_count = 0
        st.success("🧹 Chat memory cleared!")

    if st.button("Show History"):
        st.subheader("📚 Conversation History")
        history = chatbot.get_conversation_history(thread_id)
        if history:
            for msg in history:
                role = "🤖" if msg["role"] == "bot" else "👤"
                st.markdown(f"{role} **{msg['role'].capitalize()}**: {msg['content']}")
        else:
            st.info("No history yet.")

# Chat interface
st.subheader("💬 Chat With the Bot")
user_input = st.text_input("Type your message:")

if st.button("Send"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            response = chatbot.chat(user_input, thread_id=thread_id)
            st.session_state.message_count += 1
            st.success(f"🤖 Bot: {response}")
    else:
        st.warning("Please type something to send.")

# Show quick tips
if st.session_state.message_count and st.session_state.message_count % 5 == 0:
    st.info("💡 Tip: Ask about email campaigns or partnership workflows!")

