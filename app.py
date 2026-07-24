import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mental Health Support Bot", page_icon="🧠", layout="centered")

st.title("🧠 Mental Health Support Bot")
st.write("A safe space to share how you are feeling.")

# API Key setup
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing! Add it in Streamlit App Settings -> Secrets.")
    st.stop()

# Configure GenAI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Session Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
