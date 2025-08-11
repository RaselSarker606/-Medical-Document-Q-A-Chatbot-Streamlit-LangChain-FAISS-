from pypdf import PdfReader
from typing import List
import io

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text
