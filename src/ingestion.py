# src/ingestion.py
import docx
from abc import ABC, abstractmethod

class DocumentIngester(ABC):
    """Base class for document ingesters. Extend for new file types."""
    
    @abstractmethod
    def ingest(self, file_path: str) -> str:
        """Ingest the document and return raw text."""
        pass

class WordDocumentIngester(DocumentIngester):
    """Ingester for .docx files."""
    
    def ingest(self, file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            raise ValueError(f"Error ingesting {file_path}: {e}")
