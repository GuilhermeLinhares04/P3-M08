import google.generativeai as genai
import streamlit as st
import PyPDF2

# Function to read PDF content
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Read the safety guidelines PDF
safety_guidelines = read_pdf("eng_workshop.pdf") 

# API configuration
genai.configure(api_key="API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Chat with Safety Consultant")

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
    
    # Combine safety context, guidelines, and user prompt
    combined_prompt = f"""
    Context from Safety Guidelines:
    {safety_guidelines}

    Safety Expert Context:
    You are an expert industrial safety consultant. Your responses should:
    1. Be based on the safety guidelines provided
    2. Be clear and succinct
    3. Discuss emergency protocols when relevant
    4. Be polite and professional
    
    User Question: {prompt}
    
    Please provide a response based on the safety guidelines provided and your expertise.
    """
    
    # Get AI response with combined context
    response = model.generate_content(combined_prompt)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response.text)