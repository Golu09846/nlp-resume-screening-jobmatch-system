# FILE: app/services/preprocessor.py

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources once
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

class TextPreprocessor:
    def __init__(self):
        """Initialize stopwords and lemmatizer."""
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

        # Add custom stopwords for better NLP cleaning
        self.custom_job_stopwords = {
            "responsible", "requirements", "skills", "experience", "ability",
            "knowledge", "job", "role", "looking", "applicant", "candidate",
            "must", "should", "preferred", "good", "excellent", "strong"
        }

        self.stop_words = self.stop_words.union(self.custom_job_stopwords)

    def clean_text(self, text: str) -> str:
        """
        Clean text for NLP processing:
        - Lowercase
        - Remove URLs
        - Remove non-alphabet characters
        - Remove stopwords
        - Lemmatize
        """
        if not text or not isinstance(text, str):
            return ""

        # Lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r"http\S+|www\S+", " ", text)

        # Remove numbers & special chars (keep alphabets)
        text = re.sub(r"[^a-z\s]", " ", text)

        # Collapse extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Tokenize
        words = text.split()

        # Remove stopwords & lemmatize
        cleaned_words = [
            self.lemmatizer.lemmatize(word)
            for word in words
            if word not in self.stop_words
        ]

        return " ".join(cleaned_words)

    def clean_and_tokenize(self, text: str):
        """Additional helper (OPTIONAL): returns token list instead of string."""
        cleaned = self.clean_text(text)
        return cleaned.split()
