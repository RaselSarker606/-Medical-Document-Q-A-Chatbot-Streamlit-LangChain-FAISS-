import streamlit as st

def pdf_uploader():

    return st.file_uploader(
        "Upload PDF Files",
        type='pdf',
        accept_multiple_files=True,
        help="Upload one or more medical PDF documents"
    )