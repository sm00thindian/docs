# src/base_optimizer.py

from abc import ABC, abstractmethod
from typing import List, Any
import yaml

class BaseDocumentOptimizer(ABC):
    """
    Base class for document optimizers. Subclasses implement document-type-specific loading.
    """
    def __init__(self, config_path: str = "../../config.yaml"):
        """
        Initializes with config from YAML file.
        """
        self.config = self._load_config(config_path)
        self.file_extension = None  # Set by subclasses or config
        self.chunk_size = None
        self.chunk_overlap = None

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    @abstractmethod
    def load_document(self, file_path: str) -> Any:
        """
        Loads the document content.
        """
        pass

    def optimize(self, content: Any) -> List[str]:
        """
        Optimizes content: extracts text, cleans, and chunks.
        """
        text = self._extract_text(content)
        text = self._clean_text(text)
        return self._chunk_text(text)

    @abstractmethod
    def _extract_text(self, content: Any) -> str:
        """
        Extracts plain text from content.
        """
        pass

    def _clean_text(self, text: str) -> str:
        """
        Cleans text: removes extra whitespace.
        """
        return ' '.join(text.split())

    def _chunk_text(self, text: str) -> List[str]:
        """
        Splits text into chunks with overlap.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            while end < len(text) and text[end] != ' ':
                end += 1
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - self.chunk_overlap if end - self.chunk_overlap > start else start + 1
        return chunks
