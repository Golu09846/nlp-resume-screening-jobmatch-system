# FILE: app/utils/section_parser.py

import re

class SectionParser:

    # ------------------ EXTRACT EMAIL ------------------
    @staticmethod
    def extract_email(text):
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        match = re.search(pattern, text)
        return match.group(0) if match else None

    # ------------------ EXTRACT PHONE ------------------
    @staticmethod
    def extract_phone(text):
        pattern = r"(\+?\d[\d\s\-]{7,}\d)"
        match = re.search(pattern, text)
        return match.group(0) if match else None

    # ------------------ EXTRACT NAME ------------------
    @staticmethod
    def extract_name(text):
        lines = text.split("\n")

        for line in lines[:5]:   # top 5 lines usually contain the name
            clean = line.strip()

            # Remove emojis, icons, symbols except letters/spaces
            clean = re.sub(r"[^a-zA-Z\s]", "", clean)

            # Allow 1–4 word names (supports single-name resumes)
            if clean and 1 <= len(clean.split()) <= 4:
                return clean.title()

        return None


    # ------------------ EXTRACT EDUCATION ------------------
    @staticmethod
    def extract_education(text):
        edu_keywords = [
            "bachelor", "b.tech", "btech", "ba", "bs",
            "master", "m.tech", "mtech", "msc", "degree",
            "university", "college", "school", "graduation"
        ]

        lines = text.lower().split("\n")
        matches = [l for l in lines if any(k in l for k in edu_keywords)]
        return " ".join(matches) if matches else None

    # ------------------ EXTRACT EXPERIENCE ------------------
    @staticmethod
    def extract_experience(text):
        exp_keywords = ["experience", "intern", "worked", "project", "role", "position"]
        lines = text.lower().split("\n")

        matches = [l for l in lines if any(k in l for k in exp_keywords)]
        return " ".join(matches) if matches else None

    # ------------------ EXTRACT PROJECTS ------------------
    @staticmethod
    def extract_projects(text):
        proj_keywords = ["project", "developed", "built", "created"]
        lines = text.lower().split("\n")

        matches = [l for l in lines if any(k in l for k in proj_keywords)]
        return " ".join(matches) if matches else None

    # ------------------ MASTER FUNCTION ------------------
    @staticmethod
    def get_sections(text):

        return {
            "name": SectionParser.extract_name(text),
            "email": SectionParser.extract_email(text),
            "phone": SectionParser.extract_phone(text),
            "education": SectionParser.extract_education(text),
            "experience": SectionParser.extract_experience(text),
            "projects": SectionParser.extract_projects(text),
        }
