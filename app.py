import os
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="Compassionate Medical & Mental Health Assistant",
    page_icon="🩺",
    layout="centered"
)

# Custom Styling for Medical/Health Theme
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Medical Disclaimer Header
st.title("🩺 MediMind Assistant")
st.caption("Your compassionate companion for emotional well-being and health guidance.")

st.info(
    "⚠️ **Medical Disclaimer:** I am an AI-powered assistant made by Prateek Kumar Asthana of KIET , not a licensed doctor or psychiatrist. "
    "If you are experiencing a medical emergency, severe distress, or thoughts of self-harm, "
    "please contact local crisis helplines or seek immediate professional medical attention."
)

# API Key Validation
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing! Add it in Streamlit App Settings -> Secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# System Instruction for Medical / Mental Health Assistant Persona
SYSTEM_INSTRUCTION = """
You are MediMind, a compassionate, empathetic, and knowledgeable virtual Medical & Mental Health Assistant.
Your core objectives:
1. Actively listen to the user with warmth, validation, and zero judgment.
2. Provide gentle, evidence-based coping strategies (e.g., 5-4-3-2-1 grounding, box breathing, sleep hygiene, gentle self-care).
3. Use clear, accessible, and reassuring language. Avoid dense medical jargon unless explained simply inline.
4. Maintain strict safety boundaries: Always remind users gently when medical concerns require a physical examination or professional evaluation.
5. In cases of severe emotional distress, offer gentle comfort and encourage reaching out to a professional or loved ones.
"""

# Initialize Gemini Model with System Instructions
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite",
    system_instruction=SYSTEM_INSTRUCTION
)

# Initialize Session Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your virtual health assistant. How are you feeling today—both physically and emotionally?"
        }
    ]

# Render Chat History
for message in st.session_state.messages:
    avatar = "🩺" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Share how you are feeling or ask a health-related question..."):
    # Append & Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Analyzing with care..."):
            try:
                # Reconstruct conversation history for multi-turn context
                chat_history = [
                    {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                    for msg in st.session_state.messages[:-1]
                ]
                
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Something went wrong: {e}")
