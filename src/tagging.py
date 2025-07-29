# src/tagging.py
import nltk
from typing import List, Dict
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from collections import Counter

class TextTagger:
    """Handles tagging chunks. Adds metadata and simple keywords."""
    
    def tag_chunks(self, chunks: List[str], file_name: str) -> List[Dict]:
        """Tag each chunk with metadata and keywords."""
        tagged_chunks = []
        stop_words = set(stopwords.words('english'))
        
        for i, chunk in enumerate(chunks):
            words = nltk.word_tokenize(chunk.lower())
            filtered_words = [w for w in words if w.isalnum() and w not in stop_words]
            keywords = [word for word, _ in Counter(filtered_words).most_common(5)]
            
            tagged = {
                'chunk_id': i,
                'file_name': file_name,
                'content': chunk,
                'word_count': len(words),
                'keywords': keywords,
                # Add more tags here in the future (e.g., entities via spaCy)
            }
            tagged_chunks.append(tagged)
        
        return tagged_chunks
