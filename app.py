from dotenv import load_dotenv
import streamlit as st
import os
import pdf2image
import google.generativeai as genai
from pdf2image import convert_from_bytes
from PIL import Image
import io
import base64
import pdfplumber

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_gemni_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text,pdf_content,prompt])
    text_part = []
    print('Visualized response:', response) 
    for candidate in response.candidates:  
        for part in candidate.content.parts: 
            if hasattr(part, 'text'): 
                text_part.append(part.text)  
    return '\n'.join(text_part)

# def input_pdf_setup(upload_file):
#     if upload_file:
#         image = pdf2image.convert_from_bytes(upload_file.read())
#         first_image = image[0]

#         img_byte_arr = io.BytesIO()
#         first_image.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_part = {
#             'mime_type': 'image/jpeg',
#             'data': base64.b64encode(img_byte_arr).decode()
#         }
#         return pdf_part
#     else:
#         raise FileNotFoundError('No file uploaded')



def extract_text_from_upload(upload_file):
    pdf_text=""

    with pdfplumber.open(io.BytesIO(upload_file.read())) as pdf:
        for page in pdf.pages:
            pdf_text+=page.extract_text()+'\n'

    return pdf_text

    



st.set_page_config(page_title="Optimize Your Resume for ATS")
st.header("Application Tracking System")
input_text = st.text_area('Job description:', key='input_text')
upload_file = st.file_uploader('Upload your file (PDF)', type=["pdf"])

if upload_file is not None:
    st.write('File uploaded successfully...')

submit1 = st.button('Tell me about Resume')
submit2 = st.button('How can I improve my skills')
submit3 = st.button('Percentage match')

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
You are an ATS expert specializing in technical roles (Data Science, Full Stack Development, Machine Learning, DevOps, or Big Data Engineering). 
Your task is to review a resume for the specified position. Calculate the match percentage based on the candidate's skills and experiences compared to the 
job description. List any missing keywords critical for the role that are absent in the resume. Offer comprehensive feedback on the candidate's suitability, 
emphasizing strengths and suggesting improvements to optimize their application for the role.understand if work experience details is not given then the candidate is fresher
"""

input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) scanner with deep expertise in technical roles including Data Science, Full Stack Development, Machine Learning, DevOps, and Big Data Engineering. Your task is to evaluate a resume against a provided job description. Follow these steps to calculate the match score:

1. **Extract Key Responsibilities:**
   Identify and list the core responsibilities and daily tasks mentioned in the job description. Look for action verbs that describe what the candidate will be doing in the role.

2. **Extract Required Skills and Competencies:**
   Identify and list the skills and competencies required for the role as mentioned in the job description. Pay attention to terms like "required," "must-have," "desired," and "preferred" to understand the priority of each skill.


3. **Extract Qualifications and Experience:**
   Identify the qualifications and years of experience required for the role. Note any specific educational background or certifications mentioned.
   if experience details is not given then the candidate considered as fresher
4. **Compare with Resume:**
   Match the extracted responsibilities, skills, and qualifications against those mentioned in the candidate's resume. Highlight the skills and experiences that align with the job description.

5. **Calculate Match Percentage:**
   Calculate the match percentage based on the proportion of required responsibilities, skills, and qualifications present in the resume compared to those in the job description.

6. **Identify Missing Keywords:**
   List the keywords (responsibilities, skills, qualifications) mentioned in the job description that are not found in the resume.
   based on these missing keywords and its priority ,reduce the matching score.
Output Structure:

- **Match Percentage:** Example: 85%
- **Missing Keywords:** Example: ["Docker", "Kubernetes", "CI/CD", "Python"]
- **Final Thoughts:** Provide a summary of the candidate's strengths and areas for improvement, emphasizing how well their profile aligns with the job description.

Use this structured approach to ensure a thorough and accurate evaluation of the resume against the job description.
"""

if submit1:
    if upload_file is not None:
        pdf_content = extract_text_from_upload(upload_file)
        response = get_gemni_response(input_text, pdf_content, input_prompt1)
        st.subheader('The Response is:')
        st.write(response)
    else:
        st.write('Please upload the file')

if submit3:
    if upload_file is not None:
        pdf_content = extract_text_from_upload(upload_file)
        response = get_gemni_response(input_text, pdf_content, input_prompt3)
        st.subheader('The Response is:')
        st.write(response)
    else:
        st.write('Please upload the file')
