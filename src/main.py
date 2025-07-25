# src/main.py

import yaml
from .word_optimizer import WordDocumentOptimizer
from .utils import find_documents

def main():
    with open("../../config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    input_dir = config['directories']['input']
    
    # Example: Use Word optimizer
    optimizer = WordDocumentOptimizer()
    files = find_documents(input_dir, optimizer.file_extension)
    
    for file_path in files:
        print(f"Processing {file_path}")
        content = optimizer.load_document(file_path)
        chunks = optimizer.optimize(content)
        print(f"Optimized into {len(chunks)} chunks.")
        # Optionally save chunks to output dir, e.g., write to files
    
if __name__ == "__main__":
    main()
