import google.generativeai as genai
import streamlit as st

genai.configure(api_key="API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)
st.title("Chat with Gemini Flash")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    response = model.generate_content(prompt)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response.text)