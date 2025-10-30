# src/tagging.py
import nltk
import spacy
import logging
import yaml
import os
from typing import List, Dict, Set
from nltk.corpus import stopwords
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextTagger:
    """Handles tagging chunks with metadata, keywords, entities, and intents."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Load generic keywords from config.yaml."""
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        # Load spaCy model (NER-only for speed)
        self.nlp = spacy.load('en_core_web_lg', disable=['parser', 'tagger', 'lemmatizer'])
        
        # Load generic keywords from config
        self.keywords: Set[str] = set()
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                raw_keywords = config.get("keywords", [])
                self.keywords = {word.strip().lower() for word in raw_keywords if word.strip()}
                logging.info(f"Loaded {len(self.keywords)} keywords from {config_path}")
            except Exception as e:
                logging.warning(f"Failed to load keywords from {config_path}: {e}")
        else:
            logging.warning(f"Config file {config_path} not found. Using empty keyword set.")

        self.stop_words = set(stopwords.words('english'))
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
            top_keywords = [word for word, _ in Counter(filtered_words).most_common(5)]
            
            # Use config-loaded keywords
            matched_keywords = [w for w in words if w in self.keywords]
            
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
                'keywords': top_keywords,
                'matched_keywords': list(set(matched_keywords)),  # ← from config
                'entities': entities,
                'intents': intents or ['general'],
                'chunk_position': i / total_chunks if total_chunks > 0 else 0.0,
            }
        except Exception as e:
            logging.error(f"Error tagging chunk {i}: {e}")
            return {
                'chunk_id': i, 'file_name': file_name, 'content': chunk, 'error': str(e)
            }

    def tag_chunks(self, chunks: List[str], file_name: str) -> List[Dict]:
        total_chunks = len(chunks)
        if total_chunks == 0:
            return []
        tagged = [
            self._tag_single(i, chunk, file_name, total_chunks)
            for i, chunk in enumerate(chunks)
        ]
        logging.info(f"Tagged {len(tagged)} chunks for {file_name}")
        return tagged
