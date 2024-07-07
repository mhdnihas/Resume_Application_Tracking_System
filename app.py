from dotenv import load_dotenv

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
from pdf2image import convert_from_bytes
from PIL import Image
import io
import base64

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print("API Key:", api_key)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
print('hello:',genai.configure(api_key=os.getenv("GOOGLE_API_KEY")))

def get_gemni_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content,prompt])
    return response.text


def input_pdf_setup(upload_file):

    if upload_file:
        image=pdf2image.convert_from_bytes(upload_file.read())
        first_image=image[0]
        print(first_image)

        img_byte_arr=io.BytesIO()
        first_image.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()
    
        print('imag_byt_arr:',img_byte_arr)


        pdf_part={
            'mime_type':'image/jpeg',
            'data':base64.b64encode(img_byte_arr).decode()
        }
        return pdf_part
    else:
        raise FileNotFoundError('No file uploaded')



st.set_page_config(page_title="Optimize Your Resume for ATS")
st.header("Application Tracking System")
input_text=st.text_area('job description:',key=input)
upload_file=st.file_uploader('upload your file(pdf)',type=["pdf"])

if upload_file is not None:
    st.write('File Uploaded successfully...')




submit1=st.button('Tell me about Resume')

submit2=st.button('How can I improve my skills')

submit3=st.button('Percentage match')





if st.button('Optimize Resume for ATS'):
    if input_text:
        st.info('Analyzing resume...')
        
        if upload_file:
            pdf_images = convert_from_bytes(upload_file.read())
            st.image(pdf_images[0])  
        else:
            st.warning('Please upload a PDF file.')



st.sidebar.header('Tips for ATS Optimization')
st.sidebar.markdown("""
- Use keywords from the job description in your resume.
- Format your resume consistently and use clear headings.
- Quantify your achievements with numbers and percentages.
- Proofread carefully to eliminate spelling and grammar errors.
""")


st.markdown('---')





input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""


if submit1:
    if upload_file is not None:
        pdf_content=input_pdf_setup(upload_file)
        response=get_gemni_response(input_text,pdf_content,input_prompt1)
        st.subheader('The Response is:')
        st.write(response)
