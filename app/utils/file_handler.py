# FILE: app/utils/file_handler.py

import pdfplumber

def read_pdf(file):
    """Extract text from PDF safely."""
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        return text.strip()
    except:
        return ""

def read_txt(file):
    """Extract text from TXT file."""
    try:
        return file.read().decode("utf-8", errors="ignore")
    except:
        return ""

def detect_file_type(filename):
    """Returns extension of file (pdf/txt/docx)."""
    return filename.split(".")[-1].lower()

def validate_resume_file(filename):
    """Check if resume format is correct."""
    return filename.endswith(".pdf") or filename.endswith(".docx")

def validate_jd_file(filename):
    """Check if JD format is correct."""
    return filename.endswith(".pdf") or filename.endswith(".txt")
