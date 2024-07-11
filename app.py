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
genai.configure(api_key=api_key)

#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemni_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content,prompt])
    print(response)
    return response.text


def input_pdf_setup(upload_file):

    if upload_file:
        image=pdf2image.convert_from_bytes(upload_file.read())
        first_image=image[0]

        img_byte_arr=io.BytesIO()
        first_image.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()


        pdf_part={
            'mime_type':'image/jpeg',
            'data':base64.b64encode(img_byte_arr).decode()
        }
        return pdf_part
    else:
        raise FileNotFoundError('No file uploaded')



st.set_page_config(page_title="Optimize Your Resume for ATS")
st.header("Application Tracking System")
input_text=st.text_area('job description:',key='input_text')
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
 You are an experienced Technical Human Resource Manager with Tech Experience in The Field of any one job role from  Data Science,Full Stack, Web Development , Big data engineering ,
 Devops , Data Analyst, your task is to review the provided resume against the job description for these Profiles. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""


input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) scanner with deep expertise in job roles like Data Science, Web Development, Big Data Engineering, 
DevOps, and Data Analysis. Your task is to evaluate a resume against a provided job description. Follow these steps:

1.Extract Skills and Experience:
Identify and list the key skills and relevant experiences mentioned in both the job description (JD) and the resume (CV).

2.Calculate Match Percentage:
Compare the extracted skills and experience from the resume with those required in the JD.
Calculate the percentage of match based on the proportion of required skills and experiences present in the resume.

3.Identify Missing Keywords:
List the keywords (skills, qualifications, experiences) mentioned in the JD but not found in the resume.

4.Provide Final Thoughts:
Offer feedback on the overall suitability of the resume for the job, highlighting strengths and areas for improvement.
Output Structure:

Match Percentage:

Example: 85%
Missing Keywords:

Example: ["Docker", "Kubernetes", "CI/CD", "Python"]
Final Thoughts: 

Example: "The resume matches well with the job description, especially in areas like cloud infrastructure and programming. However, 
it lacks some critical DevOps skills like Docker and Kubernetes, which are crucial for the role."
"""



if submit1:
    if upload_file is not None:
        pdf_content=input_pdf_setup(upload_file)
        response=get_gemni_response(input_text,pdf_content,input_prompt1)
        st.subheader('The Response is:')
        st.write(response)
    else:
        st.write('Please upload the file')

if submit3:
    if upload_file is not None:
        pdf_content=input_pdf_setup(upload_file)
        response=get_gemni_response(input_text,pdf_content,input_prompt3)
        st.subheader('The Response is:')
        st.write(response)
    
    else:
        st.write('Please upload the file')

