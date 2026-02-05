# FILE: app/services/resume_parser.py

import pdfplumber
import docx
from app.services.preprocessor import TextPreprocessor

class ResumeParser:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

    # ------------------------------------------------------------
    # Extract text from PDF
    # ------------------------------------------------------------
    def extract_text_from_pdf(self, file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        return text.strip()

    # ------------------------------------------------------------
    # Extract text from DOCX
    # ------------------------------------------------------------
    def extract_text_from_docx(self, file):
        text = ""
        doc = docx.Document(file)
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        return text.strip()

    # ------------------------------------------------------------
    # Main → Return BOTH raw text & cleaned text
    # ------------------------------------------------------------
    def get_resume_text(self, uploaded_file):
        filename = uploaded_file.name.lower()

        # RAW TEXT
        if filename.endswith(".pdf"):
            raw_text = self.extract_text_from_pdf(uploaded_file)
        elif filename.endswith(".docx"):
            raw_text = self.extract_text_from_docx(uploaded_file)
        else:
            return None, None

        if not raw_text.strip():
            return None, None

        # CLEAN TEXT
        cleaned_text = self.preprocessor.clean_text(raw_text)

        # VERY IMPORTANT → RETURN BOTH
        return raw_text, cleaned_text
