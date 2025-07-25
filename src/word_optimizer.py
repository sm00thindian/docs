# src/word_optimizer.py

from .base_optimizer import BaseDocumentOptimizer
from docx import Document
from typing import Any

class WordDocumentOptimizer(BaseDocumentOptimizer):
    """
    Optimizer for Microsoft Word (.docx) documents.
    """
    def __init__(self, config_path: str = None):
        super().__init__(config_path)
        doc_config = self.config['document_types']['word']
        self.file_extension = doc_config['extension']
        self.chunk_size = doc_config['chunk_size']
        self.chunk_overlap = doc_config['chunk_overlap']

    def load_document(self, file_path: str) -> Document:
        return Document(file_path)

    def _extract_text(self, content: Document) -> str:
        text = [paragraph.text for paragraph in content.paragraphs]
        return '\n'.join(text)

    def _clean_text(self, text: str) -> str:
        text = super()._clean_text(text)
        lines = text.split('\n')
        cleaned_lines = [line for line in lines if line.strip() and len(line.strip()) > 5]
        return '\n'.join(cleaned_lines)
