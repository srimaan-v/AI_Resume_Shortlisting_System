import PyPDF2
import re

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text
