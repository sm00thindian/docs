# src/tagging.py
import nltk
import spacy
from typing import List, Dict
from nltk.corpus import stopwords
from collections import Counter

class TextTagger:
    """Handles tagging chunks with metadata, keywords, and entities."""
    
    def __init__(self):
        """Initialize NLTK and spaCy."""
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.nlp = spacy.load('en_core_web_sm', disable=['parser'])  # Disable unused components for speed
        self.stop_words = set(stopwords.words('english'))
    
    def tag_chunks(self, chunks: List[str], file_name: str) -> List[Dict]:
        """Tag each chunk with metadata, keywords, and entities."""
        tagged_chunks = []
        
        for i, chunk in enumerate(chunks):
            # NLTK-based keyword extraction
            words = nltk.word_tokenize(chunk.lower())
            filtered_words = [w for w in words if w.isalnum() and w not in self.stop_words]
            keywords = [word for word, _ in Counter(filtered_words).most_common(5)]
            
            # spaCy-based NER
            doc = self.nlp(chunk)
            entities = [(ent.text, ent.label_) for ent in doc.ents]  # e.g., [("HIPAA", "LAW"), ("2023", "DATE")]
            
            tagged = {
                'chunk_id': i,
                'file_name': file_name,
                'content': chunk,
                'word_count': len(words),
                'keywords': keywords,
                'entities': entities,  # New: Add named entities
            }
            tagged_chunks.append(tagged)
        
        return tagged_chunks
