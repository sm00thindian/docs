# DOCS (Document Optimization for Conversational Systems)

This is a Python-based project for optimizing documents in a Retrieval-Augmented Generation (RAG) system, specifically for a policy chatbot. The project is designed to handle file ingestion, cleaning, chunking with overlap, and tagging. It focuses on Word documents (.docx) initially but is built modularly to allow easy extension to other document types (e.g., PDF, TXT) in the future.

## Project Structure
The project is structured as a Python package suitable for a GitHub repository. Here's the layout:

docs/ 
├── README.md              # Project documentation 
├── requirements.txt       # Dependencies 
├── setup.py               # For installing as a package (optional, for future use)  
├── src/  
│   ├── init.py        # Makes src a package  
│   ├── ingestion.py       # Handles document loading  
│   ├── cleaning.py        # Handles text cleaning  
│   ├── chunking.py        # Handles chunking with overlap 
│   ├── tagging.py         # Handles tagging/metadata addition  
│   ├── pipeline.py        # Orchestrates the full process  
│   └── utils.py           # Utility functions (e.g., file handling)  
├── tests/  
│   ├── init.py
│
├── test_ingestion.py  # Unit tests for ingestion
│   ├── test_cleaning.py   # Unit tests for cleaning
│   ├── test_chunking.py   # Unit tests for chunking
│   ├── test_tagging.py    # Unit tests for tagging
│   └── test_pipeline.py   # Integration tests
├── examples/
│   └── sample_policy.docx # Sample input file (not included here; add your own)
└── output/                # Directory for processed outputs (created at runtime)

## Design Principles
- **Modularity**: Each step (ingestion, cleaning, chunking, tagging) is in its own module with extensible classes/functions. For example, ingestion uses a base `DocumentIngester` class that can be subclassed for new file types.
- **Extensibility for Future RAG Optimizations**: The pipeline is a sequence of steps that can be easily extended (e.g., add embedding generation or similarity deduplication later by adding new modules and updating the pipeline).
- **Output Format Choice**: Outputs are in JSON format. This was chosen strategically for optimal user experience because:
  - JSON is structured, allowing easy inclusion of metadata/tags with each chunk.
  - It's machine-readable and parseable for downstream RAG ingestion (e.g., into a vector DB like Pinecone or FAISS).
  - It supports extensibility (e.g., adding embeddings or scores later).
  - Compared to TXT (unstructured) or CSV (tabular but less flexible for nested data), JSON handles hierarchical data better (e.g., chunks with overlap info and tags).
- **Focus on Word Docs**: Uses `python-docx` for .docx files. Future extensions can add libraries like `PyPDF2` for PDFs.
- **Chunking**: Default chunk size 500 words, overlap 100 words (configurable).
- **Tagging**: Adds basic metadata (file name, chunk ID, word count) and simple tags (e.g., extracted keywords using NLTK). Extensible for more advanced tagging (e.g., NLP-based entity recognition).
- **Error Handling**: Basic try-except blocks; logging for debugging.
- **Dependencies**: Minimal, listed in `requirements.txt`.

## Installation
1. Clone the repo: `git clone https://github.com/sm00thindian/docs.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the pipeline: `python src/pipeline.py --input_dir path/to/docs --output_dir output/ [--output_pdf]`

## Usage
- Run the full pipeline from `pipeline.py`.
- Customize parameters like chunk_size, overlap, etc., via command-line args.
- Outputs: A JSON file per input document, e.g., `output/sample_policy.json` containing a list of chunk objects.

## Future Extensions
- Add new ingesters (e.g., PDFIngester) by subclassing `DocumentIngester`.
- Add new pipeline steps (e.g., deduplication) by appending to the `process_document` method.
- Enhance tagging with ML models (e.g., spaCy for NER).
- Support batch processing for large directories.
