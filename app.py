import openai
import streamlit as st
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit UI
st.title("GenAI PDF Chatbot")

# File uploader
pdf_file = st.file_uploader("Upload a PDF", type="pdf")

if pdf_file is not None:
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()

    st.write("PDF content loaded. Now ask me anything!")

    # User input for questions
    user_question = st.text_input("Ask a question about the PDF:")

    # Add a button to trigger the answer generation
    if st.button("Get Answer"):
        if user_question:
            # OpenAI API request with the newer model
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Answer the following question based on the content of the PDF: {user_question}.\n\n{text}"}
                ]
            )
            answer = response['choices'][0]['message']['content']
            st.write(answer)
        else:
            st.warning("Please enter a question before clicking the button.")
