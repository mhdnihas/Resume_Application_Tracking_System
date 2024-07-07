from dotenv import load_dotenv

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai


from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemni_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content,prompt])
    return response.text


st.set_page_config(page_title="Optimize Your Resume for ATS")
st.header("Application Tracking System")
input_text=st.text_area('job description:',key=input)
upload_file=st.file_uploader('upload your file(pdf)',type=["pdf"])