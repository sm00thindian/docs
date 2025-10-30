# src/tagging.py
import nltk
import spacy
import logging
from typing import List, Dict
from nltk.corpus import stopwords
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextTagger:
    """Handles tagging chunks with metadata, keywords, entities, and intents."""
    
    def __init__(self, nlp=None):
        """Accept pre-loaded spaCy model to avoid loading in workers."""
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.nlp = nlp or spacy.load('en_core_web_lg', disable=['parser', 'tagger', 'lemmatizer'])
        self.stop_words = set(stopwords.words('english'))
        self.POLICY_KEYWORDS = {
            'compliance', 'regulation', 'policy', 'audit', 'governance', 'privacy',
            'security', 'data protection', 'GDPR', 'HIPAA', 'standard', 'SAFR', 'guideline'
        }
        self.INTENT_PATTERNS = {
            'rule': ['must', 'shall', 'required', 'prohibited'],
            'definition': ['defined as', 'means', 'refers to'],
            'procedure': ['step', 'process', 'procedure']
        }
        logging.info("TextTagger initialized (NER-only spaCy)")

    def _tag_single(self, i: int, chunk: str, file_name: str, total_chunks: int) -> Dict:
        try:
            words = nltk.word_tokenize(chunk.lower())
            filtered_words = [w for w in words if w.isalnum() and w not in self.stop_words]
            keywords = [word for word, _ in Counter(filtered_words).most_common(5)]
            policy_keywords = [w for w in words if w.lower() in self.POLICY_KEYWORDS]
            doc = self.nlp(chunk)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            chunk_lower = chunk.lower()
            intents = [
                intent for intent, markers in self.INTENT_PATTERNS.items()
                if any(marker in chunk_lower for marker in markers)
            ]
            return {
                'chunk_id': i,
                'file_name': file_name,
                'content': chunk,
                'word_count': len(words),
                'keywords': keywords,
                'entities': entities,
                'policy_keywords': list(set(policy_keywords)),
                'intents': intents or ['general'],
                'chunk_position': i / total_chunks if total_chunks > 0 else 0.0,
            }
        except Exception as e:
            logging.error(f"Error tagging chunk {i}: {e}")
            return {
                'chunk_id': i, 'file_name': file_name, 'content': chunk, 'error': str(e)
            }

    def tag_chunks(self, chunks: List[str], file_name: str) -> List[Dict]:
        """Sequential tagging – safe inside daemon workers."""
        total_chunks = len(chunks)
        if total_chunks == 0:
            return []
        tagged = [self._tag_single(i, chunk, file_name, total_chunks) for i, chunk in enumerate(chunks)]
        logging.info(f"Tagged {len(tagged)} chunks for {file_name}")
        return tagged
