def load_document(self, file_path):
    try:
        return Document(file_path)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def extract_metadata(self, content):
    """
    Extracts metadata from the document.
    """
    core_props = content.core_properties
    metadata = {
        'title': core_props.title,
        'author': core_props.author,
        'created': str(core_props.created),
        'modified': str(core_props.modified),
        'keywords': core_props.keywords
    }
    return metadata

def optimize(self, content):
    """
    Optimizes the document: extracts metadata, removes headers/footers, hierarchical chunking based on headings, paragraphs, and tables.
    """
    if content is None:
        return []

    metadata = self.extract_metadata(content)
    chunks = []
    current_heading = "No Heading"
    current_section_chunks = []

    # Extract paragraphs with heading hierarchy
    for paragraph in content.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            if current_section_chunks:
                chunks.append({
                    'text': '\n'.join(current_section_chunks),
                    'metadata': {**metadata, 'heading': current_heading, 'type': 'section'}
                })
                current_section_chunks = []
            current_heading = paragraph.text.strip()
        else:
            text = paragraph.text.strip()
            if text:
                current_section_chunks.append(self._clean_text(text))

    if current_section_chunks:
        chunks.append({
            'text': '\n'.join(current_section_chunks),
            'metadata': {**metadata, 'heading': current_heading, 'type': 'section'}
        })

    # Extract tables as separate chunks
    for table in content.tables:
        table_chunk = self._table_to_markdown(table)
        if table_chunk:
            chunks.append({
                'text': table_chunk,
                'metadata': {**metadata, 'type': 'table'}
            })

    return chunks

def extract_removed(self, content):
    """
    Extracts removed sections: headers and footers as chunks.
    """
    removed_chunks = []

    # Extract headers and footers from sections
    for section in content.sections:
        # Headers
        for paragraph in section.header.paragraphs:
            text = paragraph.text.strip()
            if text:
                removed_chunks.append(text)
        # Footers
        for paragraph in section.footer.paragraphs:
            text = paragraph.text.strip()
            if text:
                removed_chunks.append(text)

    return removed_chunks

def _table_to_markdown(self, table):
    """
    Converts a table to markdown format.
    """
    markdown = []
    # Header row
    header = [cell.text.strip() for cell in table.rows[0].cells]
    markdown.append('| ' + ' | '.join(header) + ' |')
    markdown.append('| ' + '--- | ' * len(header))

    # Data rows
    for row in table.rows[1:]:
        data = [cell.text.strip() for cell in row.cells]
        markdown.append('| ' + ' | '.join(data) + ' |')

    return '\n'.join(markdown)

def _clean_text(self, text):
    # Enhanced cleaning: remove special characters, normalize
    text = super()._clean_text(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()  # Remove punctuation, lowercase
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if line.strip() and len(line.strip()) > 5]
    return '\n'.join(cleaned_lines)

def _extract_text(self, content):
    """
    Extracts plain text from the document content.
    Note: This method is implemented to satisfy the abstract base class requirement,
    but is not used in the custom optimize() for Word documents.
    """
    full_text = []
    for paragraph in content.paragraphs:
        full_text.append(paragraph.text.strip())
    for table in content.tables:
        for row in table.rows:
            full_text.append(' '.join(cell.text.strip() for cell in row.cells))
    return '\n'.join(full_text)
