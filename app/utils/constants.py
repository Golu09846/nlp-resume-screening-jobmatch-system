# FILE: app/utils/constants.py

# Supported resume formats
SUPPORTED_RESUME_TYPES = ["pdf", "docx"]

# Supported JD formats
SUPPORTED_JD_TYPES = ["txt", "pdf"]

# Global skill vocabulary for skill extraction
SKILL_VOCAB = {
    "python", "sql", "mysql", "nlp", "machine learning", "ml",
    "deep learning", "pandas", "numpy", "matplotlib", "seaborn",
    "statistics", "probability", "data analysis", "nltk",
    "tensorflow", "pytorch", "git", "github"
}

# Common JD noise words
JD_NOISE_WORDS = {
    "responsible", "excellent", "requirements", "preferred",
    "strong", "ability", "knowledge", "should", "must",
    "candidate", "applicant", "looking"
}
