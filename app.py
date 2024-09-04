import streamlit as st
import time
from utils import query_emergency, get_eta, llm_generation

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'state' not in st.session_state:
        st.session_state.state = "awaiting_message_type"
    if 'emergency_description' not in st.session_state:
        st.session_state.emergency_description = None
    if 'emergency_response' not in st.session_state:
        st.session_state.emergency_response = None
    if 'location' not in st.session_state:
        st.session_state.location = None
    if 'eta' not in st.session_state:
        st.session_state.eta = None
    if 'emergency_start_time' not in st.session_state:
        st.session_state.emergency_start_time = None

def get_llm_response(instruction, user_input=None):
    prompt = f"{instruction}\n\nUser: {user_input}" if user_input else instruction
    return llm_generation(prompt)

def main():
    st.title("Dr. Adrian's AI Receptionist")
    initialize_session_state()

    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])

    if st.session_state.state == "awaiting_message_type" and not st.session_state.messages:
        initial_greeting = get_llm_response("Greet the user and ask if they are experiencing an emergency or would like to leave a message. Keep the response concise.")
        st.chat_message("assistant").write(initial_greeting)
        st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        if st.session_state.state == "awaiting_message_type":
            instruction = "Determine if the user is experiencing an emergency or wants to leave a message. If it's an emergency, ask for a clear description. If it's a message, ask them to provide it. If unclear, ask for clarification. Keep the response concise."
            response = get_llm_response(instruction, user_input)
            if "emergency" in user_input.lower():
                st.session_state.state = "awaiting_emergency_description"
            elif "message" in user_input.lower():
                st.session_state.state = "awaiting_message"
        elif st.session_state.state == "awaiting_emergency_description":
            st.session_state.emergency_description = user_input
            st.session_state.state = "awaiting_location"
            st.session_state.emergency_start_time = time.time()
            instruction = "Acknowledge the emergency description and ask for the user's current location. Emphasize the importance of this information for providing assistance. Keep the response concise."
            response = get_llm_response(instruction, user_input)
        elif st.session_state.state == "awaiting_location":
            st.session_state.location = user_input
            st.session_state.eta = get_eta("Northeast Los Angeles", user_input)
            st.session_state.state = "awaiting_eta_response"
            instruction = f"Inform the user that Dr. Adrian's ETA is {st.session_state.eta}. Ask if this is too late for their emergency situation. Request a Yes or No answer. Keep the response concise."
            response = get_llm_response(instruction)
        elif st.session_state.state == "awaiting_eta_response":
            if "yes" in user_input.lower():
                instruction = "Acknowledge that the ETA might be too long. Inform the user that you'll provide emergency instructions shortly. Reassure them and ask them to stay calm. Keep the response concise."
                response = get_llm_response(instruction)
                st.session_state.state = "processing_emergency"
            elif "no" in user_input.lower():
                instruction = "Express relief that the ETA is acceptable. Reassure the user that Dr. Adrian will arrive soon and advise them to stay calm. Keep the response concise."
                response = get_llm_response(instruction)
                st.session_state.state = "awaiting_message_type"
            else:
                instruction = "Politely ask the user to clarify with a Yes or No answer regarding whether the ETA is too late. Keep the response concise."
                response = get_llm_response(instruction)
        elif st.session_state.state == "awaiting_message":
            instruction = "Confirm receipt of the message for Dr. Adrian. Assure the user it will be delivered promptly. Ask if there's anything else they need assistance with. Keep the response concise."
            response = get_llm_response(instruction, user_input)
            st.session_state.state = "awaiting_message_type"
        else:
            response = get_llm_response("Respond to the user's input appropriately based on the context of the conversation. Keep the response concise.", user_input)

        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.session_state.state == "processing_emergency":
        with st.empty():
            for i in range(15):
                st.write(f"Processing emergency... {15-i} seconds remaining")
                time.sleep(1)
                st.empty()
            
            emergency_response = query_emergency(st.session_state.emergency_description)
            st.session_state.emergency_response = emergency_response
            instruction = f"Provide emergency instructions based on the following: {emergency_response}. Reassure the user and emphasize the importance of following these steps until Dr. Adrian arrives. Keep the response concise but clear."
            response = get_llm_response(instruction)
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.state = "awaiting_message_type"

if __name__ == "__main__":
    main()

