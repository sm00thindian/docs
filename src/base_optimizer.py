def _load_config(self, config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

@abstractmethod
def load_document(self, file_path):
    """
    Loads the document content.
    """
    pass

def optimize(self, content):
    """
    Optimizes content: extracts text, cleans, and chunks.
    """
    text = self._extract_text(content)
    text = self._clean_text(text)
    return self._chunk_text(text)

@abstractmethod
def _extract_text(self, content):
    """
    Extracts plain text from content.
    """
    pass

def _clean_text(self, text):
    """
    Cleans text: removes extra whitespace.
    """
    return ' '.join(text.split())

def _chunk_text(self, text):
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
