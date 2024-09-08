import os
import requests
import pinecone
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MAPS_API_KEY = os.getenv('MAPS_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')

# Configure Google API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index = pc.Index("emergency-index")

@st.cache_resource
def get_pinecone_index():
    return index

def embed_text(text):
    return pc.inference.embed(
        "multilingual-e5-large",
        [text],
        parameters={"input_type": "passage"}
    )[0]['values']

def query_emergency(emergency_query, similarity_threshold=0.88):
    query_vector = embed_text(emergency_query)
    
    result = index.query(
        vector=query_vector,
        top_k=1,  
        include_metadata=True
    )
    
    if result['matches'] and result['matches'][0]['score'] > similarity_threshold:
        print(f"Similarity score: {result['matches'][0]['score']}")
        next_step = result['matches'][0]['metadata']['next_step']
        return f"Next step: {next_step}"
    else:
        return "No matching emergency found."

def get_eta(source, dest):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    params = {
        'origins': source,
        'destinations': dest,
        'key': MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    duration = data['rows'][0]['elements'][0]['duration']['text']
    return duration

def get_llm_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b-exp-0827",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
    )

def get_system_prompt():
    return """
    You are an AI receptionist for Dr. Adrian, tasked with assisting users in both emergency and non-emergency situations. Your responsibilities include:

    1. **Handling Emergencies**:
       - Prompt the user to confirm if they are experiencing an emergency or if they want to leave a message.
       - If it's an emergency, guide the user to describe the situation clearly.
       - Utilize the Pinecone vector database to match the user's emergency description with the closest known emergency scenarios.
       - Provide immediate, clear, and actionable steps to the user based on the matched emergency scenario.
       - During the database query, ask the user for their current location and provide an estimated time of arrival for Dr. Adrian.
       - If the estimated time of arrival is too long, reassure the user and emphasize the importance of following the provided emergency steps until help arrives.
       - If no match is found, calmly inform the user and suggest general safety measures until Dr. Adrian can assist further.

    2. **Managing Non-Emergency Inquiries**:
       - If the user opts to leave a message, ask them to provide the message clearly.
       - Confirm receipt of the message and reassure the user that it will be forwarded to Dr. Adrian.
       - Handle unrelated or unclear user inputs by politely requesting clarification and guiding the conversation back to determining whether it's an emergency or a non-emergency inquiry.

    3. Maintaining a Professional and Calm Demeanor:
       - Always remain professional, empathetic, and calm, especially in emergency situations.
       - Use polite language and ensure that the user feels heard and supported.
       - Prioritize the user's safety and well-being in all interactions.

    4. **General Information and Appointment Scheduling**:
       - Provide accurate information about Dr. Adrian's services, scheduling, and other non-emergency queries.
    make the responses as short as possible
    """

def llm_generation(user_input):
    model = get_llm_model()
    system_prompt = get_system_prompt()

    chat_session = model.start_chat(
        history=[{
            "role": "model",
            "parts": system_prompt
        }]
    )

    response = chat_session.send_message(user_input)
    return response.text

def analyze_sentiment(text):
    model = get_llm_model()
    prompt = f"Analyze the sentiment and intent of the following text. Determine if it's an emergency, a message for Dr. Adrian, a medical question, or something else. Text: {text}"
    response = model.generate_content(prompt)
    return response.text

def get_situation_awareness(context):
    model = get_llm_model()
    prompt = f"Based on the following conversation context, determine the current situation and what information or action is needed next. Context: {context}"
    response = model.generate_content(prompt)
    return response.text