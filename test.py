import streamlit as st
from PyPDF2 import PdfReader

with st.form("User Input"):
    fileName = st.file_uploader("file")
    button = st.form_submit_button("Generate MCQs")
    print(button)

    try:
        if button and fileName is not None:
            pdf = PdfReader(fileName)
            data = ""

            if pdf:
                for page in pdf.pages:
                    data += page.extract_text()

            print(data)
    except Exception as e:
        raise Exception("error reading the pdf file")