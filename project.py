import os
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load secret key from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

client = genai.Client(api_key=GEMINI_API_KEY)


# Rest of your script...
TARGET_MODEL = "gemini-3.5-flash"

# Strict system instructions enforcing professional English and medical boundaries
SYSTEM_INSTRUCTION = """
You are a formal, professional, and empathetic mental health wellness assistant. 
Your primary objective is to listen attentively and provide non-clinical coping strategies (e.g., grounding exercises, diaphragmatic breathing, structured journaling). 
MANDATORY CONSTRAINTS:
1. You are an AI, not a licensed clinician. You must never offer medical advice, diagnostic evaluations, or clinical interpretations.
2. Never reference, suggest, or prescribe pharmacological treatments or specific medications.
3. Keep responses objective, structured, and framed within clear behavioral boundaries.
4. If severe psychological distress, self-harm intentions, or active crises are detected, instantly instruct the individual to contact official emergency services.
"""

# 2. Programmatic Safety Layer and Routing Logic
def mental_health_bot(user_message, history):
    user_msg_lower = user_message.lower()
    
    # RULE A: Immediate Crisis Override
    crisis_keywords = ["suicide", "kill myself", "hurt myself", "crisis", "end my life", "suicidal", "self-harm"]
    if any(keyword in user_msg_lower for keyword in crisis_keywords):
        return ("I am an artificial intelligence and am not equipped to handle emergencies or provide clinical intervention. "
                "If you are experiencing a crisis or imminent danger, please contact your local emergency services or call/text "
                "the Suicide & Crisis Lifeline at 988 immediately. Professional personnel are available to assist you.")

    # RULE B: Structured Screening Redirection
    screening_keywords = ["test", "screening", "quiz", "phq", "gad"]
    if any(keyword in user_msg_lower for keyword in screening_keywords):
        return ("For objective psychological assessments, clinically validated metrics such as the PHQ-9 (Depression) "
                "or GAD-7 (Anxiety) scales are required. I am unable to compute or record diagnostic scores programmatically. "
                "Please consult a certified mental health professional for formal evaluations. Let me know if you would like "
                "to focus on immediate, general grounding techniques instead.")

    # RULE C: Prescriptive Blockade
    medical_keywords = ["medicine", "medication", "diagnose", "prescription", "xanax", "antidepressant", "dosage"]
    if any(keyword in user_msg_lower for keyword in medical_keywords):
        return ("Pharmacological consultations, diagnostic verifications, and drug prescriptions fall strictly within "
                "the scope of professional medical practices. Please consult a licensed psychiatrist or primary care physician for these inquiries.")

    # Standard Execution Pipeline utilizing the Gemini 3.5 Flash Model
    try:
        response = client.models.generate_content(
            model=TARGET_MODEL, 
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        return response.text
    except Exception as e:
        return f"A system configuration error occurred. Please attempt your query again. (Diagnostic Info: {str(e)})"

# 3. Gradio Interface Layout Formulation
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Automated Mental Health & Wellness Support Interface")
    gr.Markdown(
        "**Legal Disclaimer:** This system is an automated wellness companion optimized for psychoeducation "
        "and basic coping mechanisms. It does not provide clinical diagnoses, psychiatric treatment, or crisis intervention. "
        "Running on the **Gemini 3.5 Flash** engine made by Prateek."
    )
    
    gr.ChatInterface(
        fn=mental_health_bot,
        examples=[
            "I am experiencing acute situational anxiety.", 
            "Provide instructions for a structured diaphragmatic breathing exercise.", 
            "What are the benefits of daily cognitive journaling?"
        ]
    )

# 4. Runtime Initialization with Forced Fresh Port Assignment
if __name__ == "__main__":
    demo.launch(share=True)