import streamlit as st  
from PyPDF2 import PdfReader

st.title("Pdf Text Extractor")

uploaaded_file = st.file_uploader ("Upload a File",type = ['pdf'])

if uploaaded_file is not None:

    reader=PdfReader(uploaaded_file)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    st.subheader("Extracted Text")


    st.text_area("Pdf Text",text,height = 450)