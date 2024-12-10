import streamlit as st
from pdf2image import convert_from_bytes
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import tempfile

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("AIzaSyC0nVTA7WKbDaqEpUgnseVxJiFWPr3XuKg"))

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image,prompt])
    return response.text

def convert_pdf_to_images(uploaded_files):
    images = []
    filenames = []
    for file in uploaded_files:
        filename = file.name
        filenames.append(filename)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file.seek(0)
            images += convert_from_bytes(temp_file.read())
    return images, filenames

## Streamlit App

st.set_page_config(page_title="Resume Genius")

st.image("Logo.png", width=300)
st.header("🐠 GENERATIVE AI BASED RECRUITMENT ASSISTANCE  " )
input_text=st.text_area("Job Description: ",key="input")
uploaded_files=st.file_uploader("Upload your resume(PDF)...",type=["pdf"],accept_multiple_files=True)


if uploaded_files is not None:
    st.write("PDF Uploaded Successfully")



submit1 = st.button("Resume Analysis")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Match-Rate")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight only the strengths and weaknesses of the applicant in relation to the specified job requirements. 
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_files is not None:
        imagefiles, filenames=convert_pdf_to_images(uploaded_files)
        # Display the processed images
        for i, image in enumerate(imagefiles):
            st.image(image, caption=f"{filenames[i]} - Page {i+1}")
            response=get_gemini_response(input_prompt1,image,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_files is not None:
        imagefiles, filenames=convert_pdf_to_images(uploaded_files)
        # Display the processed images
        for i, image in enumerate(imagefiles):
            st.image(image, caption=f"{filenames[i]} - Page {i+1}")
            response=get_gemini_response(input_prompt3,image,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
    else:
        st.write("Please uplaod the resume")

