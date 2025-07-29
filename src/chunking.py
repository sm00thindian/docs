# src/chunking.py
from typing import List

class TextChunker:
    """Handles chunking with overlap. Configurable sizes."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str) -> List[str]:
        """Split text into chunks with overlap."""
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)
            start += self.chunk_size - self.overlap
            if start >= end:
                break
        return chunks
