# DOCS (Document Optimization and Chunking System)
## RAG Document Optimizer

This is a modular Python package for finding, loading, and optimizing documents for Retrieval Augmented Generation (RAG) pipelines. It supports extensibility for adding new document types by creating new optimizer classes.

Updates in this version:
- Added `requirements.txt` to list all dependencies.
- Added `setup.sh` script to create a virtual environment (venv), activate it, and install dependencies from `requirements.txt`.

## Usage
1.  Make the setup script executable (if needed): chmod +x setup.sh.
2.  Run the setup script: ./setup.sh. This will create and activate a venv, and install dependencies.
3.  Place your documents in the configured input directory (e.g., ./sample_docs).
4.  Run the main script: python src/main.py (while venv is active).
