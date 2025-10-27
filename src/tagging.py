# src/tagging.py
import nltk
import spacy
import logging
from typing import List, Dict
from nltk.corpus import stopwords
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextTagger:
    """Handles tagging chunks with metadata, keywords, entities, and intents."""
    
    def __init__(self):
        """Initialize NLTK and spaCy, load stopwords and policy-specific keywords."""
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        try:
            self.nlp = spacy.load('en_core_web_lg', disable=['parser'])  # Disable parser for speed
        except Exception as e:
            logging.error(f"Failed to load spaCy model: {e}")
            raise
        self.stop_words = set(stopwords.words('english'))
        self.POLICY_KEYWORDS = {
            'compliance', 'regulation', 'policy', 'audit', 'governance', 'privacy',
            'security', 'data protection', 'GDPR', 'HIPAA', 'standard'
        }
        self.INTENT_PATTERNS = {
            'rule': ['must', 'shall', 'required', 'prohibited'],
            'definition': ['defined as', 'means', 'refers to'],
            'procedure': ['step', 'process', 'procedure']
        }
        logging.info("TextTagger initialized with spaCy and NLTK.")
    
    def tag_chunks(self, chunks: List[str], file_name: str) -> List[Dict]:
        """Tag each chunk with metadata, keywords, entities, policy keywords, and intents."""
        try:
            tagged_chunks = []
            # Batch process chunks with spaCy for efficiency
            docs = list(self.nlp.pipe(chunks))
            
            for i, (chunk, doc) in enumerate(zip(chunks, docs)):
                try:
                    # Tokenize and extract keywords with NLTK
                    words = nltk.word_tokenize(chunk.lower())
                    filtered_words = [w for w in words if w.isalnum() and w not in self.stop_words]
                    keywords = [word for word, _ in Counter(filtered_words).most_common(5)]
                    
                    # Extract policy-specific keywords
                    policy_keywords = [word for word in words if word.lower() in self.POLICY_KEYWORDS]
                    
                    # Extract named entities with spaCy
                    entities = [(ent.text, ent.label_) for ent in doc.ents]
                    
                    # Determine chunk intent based on patterns
                    chunk_lower = chunk.lower()
                    intents = [intent for intent, markers in self.INTENT_PATTERNS.items()
                              if any(marker in chunk_lower for marker in markers)]
                    
                    # Create tagged chunk
                    tagged = {
                        'chunk_id': i,
                        'file_name': file_name,
                        'content': chunk,
                        'word_count': len(words),
                        'keywords': keywords,
                        'entities': entities,
                        'policy_keywords': list(set(policy_keywords)),  # Deduplicate
                        'intents': intents if intents else ['general'],
                        'chunk_position': i / len(chunks) if chunks else 0.0,  # Normalized position (0 to 1)
                    }
                    tagged_chunks.append(tagged)
                except Exception as e:
                    logging.error(f"Error tagging chunk {i} in {file_name}: {e}")
                    tagged_chunks.append({
                        'chunk_id': i,
                        'file_name': file_name,
                        'content': chunk,
                        'error': str(e)
                    })
            
            logging.info(f"Tagged {len(tagged_chunks)} chunks for {file_name}")
            return tagged_chunks
        except Exception as e:
            logging.error(f"Failed to tag chunks for {file_name}: {e}")
            raise
