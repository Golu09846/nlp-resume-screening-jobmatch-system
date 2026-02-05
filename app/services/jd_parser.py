# FILE: app/services/jd_parser.py

from app.services.preprocessor import TextPreprocessor
import re

class JDParser:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

        # Common skills vocabulary (expandable)
        self.skills_list = {
            "python", "sql", "mysql", "nlp", "machine learning", "ml", 
            "deep learning", "pandas", "numpy", "matplotlib", "seaborn",
            "statistics", "probability", "data analysis", "nltk",
            "tensorflow", "pytorch", "communication", "problem solving"
        }

    # --------------------------------------------------------
    # Extract skills from JD (Keyword Matching)
    # --------------------------------------------------------
    def extract_skills(self, text: str):
        text_lower = text.lower()
        extracted = [skill for skill in self.skills_list if skill in text_lower]
        return list(set(extracted))  # unique skills

    # --------------------------------------------------------
    # Extract job role (very useful for score weighting)
    # --------------------------------------------------------
    def extract_role(self, text: str):
        text_lower = text.lower()
        patterns = [
            r"data analyst",
            r"nlp engineer",
            r"machine learning engineer",
            r"ai engineer",
            r"python developer",
            r"data scientist",
            r"intern"
        ]

        for p in patterns:
            match = re.search(p, text_lower)
            if match:
                return match.group(0)

        return "unknown role"

    # --------------------------------------------------------
    # Main JD Processing Function
    # --------------------------------------------------------
    def process_jd(self, jd_text: str):
        """
        Clean JD + extract skills + detect job role.
        Returns: dict {clean_text, skills, role}
        """
        if not jd_text or not jd_text.strip():
            return {
                "clean_text": "",
                "skills": [],
                "role": "unknown role"
            }

        # Clean text for embeddings
        clean_text = self.preprocessor.clean_text(jd_text)

        # Extract required skills
        jd_skills = self.extract_skills(jd_text)

        # Detect job role
        job_role = self.extract_role(jd_text)

        return {
            "clean_text": clean_text,
            "skills": jd_skills,
            "role": job_role
        }
