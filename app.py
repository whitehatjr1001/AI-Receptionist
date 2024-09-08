import streamlit as st
from utils import query_emergency, get_eta, llm_generation

def initialize_session_state():
    st.session_state.messages = []
    st.session_state.state = "awaiting_message_type"
    st.session_state.emergency_description = None
    st.session_state.emergency_response = None
    st.session_state.location = None
    st.session_state.eta = None

def get_conversation_history():
    return "\n".join([f"{role}: {content}" for role, content in st.session_state.messages])

def get_llm_response(instruction, user_input=None):
    conversation_history = get_conversation_history()
    prompt = f"Conversation history:\n{conversation_history}\n\nCurrent state: {st.session_state.state}\n\nInstruction: {instruction}\n\nUser: {user_input}"
    return llm_generation(prompt)

def main():
    st.title("Dr. Adrian's AI Medical Assistant")
    
    if 'initialized' not in st.session_state:
        initialize_session_state()
        st.session_state.initialized = True

    for role, content in st.session_state.messages:
        st.chat_message(role).write(content)

    if st.session_state.state == "awaiting_message_type" and not st.session_state.messages:
        initial_greeting = get_llm_response("Greet the user as Dr. Adrian's AI assistant and ask if they are experiencing an emergency or would like to leave a message. Keep the response concise and professional.")
        st.chat_message("assistant").write(initial_greeting)
        st.session_state.messages.append(("assistant", initial_greeting))

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append(("user", user_input))
        st.chat_message("user").write(user_input)

        if any(word in user_input.lower() for word in ["no", "nothing", "stop", "end"]):
            st.session_state.state = "ending_conversation"
            instruction = "The user wants to end the conversation. Provide a polite closing statement. Keep the response concise and professional."
        elif st.session_state.state == "awaiting_message_type":
            if "emergency" in user_input.lower():
                st.session_state.state = "awaiting_emergency_description"
                instruction = "Ask the user to describe the emergency in detail. Emphasize the importance of clear information. Keep the response concise and professional."
            elif "message" in user_input.lower():
                st.session_state.state = "awaiting_message"
                instruction = "Ask the user to provide their message for Dr. Adrian. Keep the response concise and professional."
            else:
                instruction = "The user didn't specify if it's an emergency or a message. Ask for clarification. Keep the response concise and professional."
        elif st.session_state.state == "awaiting_emergency_description":
            st.session_state.emergency_description = user_input
            st.session_state.state = "awaiting_location"
            instruction = "Acknowledge the emergency description. Ask for the user's current location to estimate Dr. Adrian's arrival time. Keep the response concise and reassuring."
        elif st.session_state.state == "awaiting_location":
            st.session_state.location = user_input
            st.session_state.eta = get_eta("Northeast Los Angeles", user_input)
            st.session_state.state = "awaiting_eta_response"
            instruction = f"Inform the user that Dr. Adrian's estimated time of arrival is {st.session_state.eta} minutes. Ask if this is too late for their emergency, requesting a clear 'Yes' or 'No' answer. Keep the response concise and professional."
        elif st.session_state.state == "awaiting_eta_response":
            if user_input.lower() == 'yes':
                st.session_state.emergency_response = query_emergency(st.session_state.emergency_description)
                instruction = f"Based on the emergency response: {st.session_state.emergency_response}, provide immediate, detailed instructions to the user. Include specific actions to take and symptoms to monitor. Emphasize the importance of following these steps until professional help arrives. Keep the response clear and reassuring."
                st.session_state.state = "emergency_follow_up"
            elif user_input.lower() == 'no':
                st.session_state.emergency_response = query_emergency(st.session_state.emergency_description)
                instruction = f"Acknowledge that the user is okay with the ETA. As a precaution, based on the emergency response: {st.session_state.emergency_response}, provide general advice and things to monitor. Keep the response calm and reassuring."
                st.session_state.state = "awaiting_message_type"
            else:
                instruction = "The user didn't provide a clear Yes or No answer. Politely ask again if Dr. Adrian's ETA is too late for their emergency, emphasizing the need for a Yes or No response."
        elif st.session_state.state == "emergency_follow_up":
            instruction = f"The user is asking a follow-up question about the emergency: '{user_input}'. Based on the previous emergency response: {st.session_state.emergency_response}, provide a detailed and relevant answer. Keep the response clear, concise, and focused on the emergency situation."
        elif st.session_state.state == "awaiting_message":
            instruction = "Confirm receipt of the message for Dr. Adrian. Assure the user it will be delivered promptly. Ask if there's anything else they need assistance with. Keep the response concise and professional."
            st.session_state.state = "awaiting_message_type"
        else:
            instruction = "Respond to the user's input appropriately based on the context of the conversation. If they need further assistance, offer help. Keep the response concise and professional."

        response = get_llm_response(instruction, user_input)
        st.chat_message("assistant").write(response)
        st.session_state.messages.append(("assistant", response))

        if st.session_state.state == "ending_conversation":
            st.stop()

    if st.button("Start New Conversation"):
        initialize_session_state()
        st.rerun()

if __name__ == "__main__":
    main()

