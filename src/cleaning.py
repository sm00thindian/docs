# src/cleaning.py
import re
import string

class TextCleaner:
    """Handles text cleaning. Extensible for custom cleaning rules."""
    
    def clean(self, text: str) -> str:
        """Clean the text: remove extra whitespace, punctuation, etc."""
        # Remove multiple whitespaces
        text = re.sub(r'\s+', ' ', text)
        # Remove punctuation (optional; keep for policies if needed)
        # text = text.translate(str.maketrans('', '', string.punctuation))
        # Lowercase (optional; policies may be case-sensitive)
        # text = text.lower()
        # Add more rules here in the future (e.g., remove headers/footers via regex)
        return text.strip()
