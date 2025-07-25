# src/main.py

import json
from src.word_optimizer import WordDocumentOptimizer  # Absolute import
from src.utils import find_documents
import os  # Added for path handling
import sys

# Add project root to sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    # Calculate project root: parent of src/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.json')
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    input_dir = config['directories']['input']
    output_dir = config['directories']['output']
    os.makedirs(output_dir, exist_ok=True)
    
    # Example: Use Word optimizer
    optimizer = WordDocumentOptimizer()
    files = find_documents(input_dir, optimizer.file_extension)
    
    for file_path in files:
        print(f"Processing {file_path}")
        content = optimizer.load_document(file_path)
        chunks = optimizer.optimize(content)
        print(f"Optimized into {len(chunks)} chunks.")
        
        # Save chunks to output dir
        for i, chunk in enumerate(chunks, 1):
            chunk_file = os.path.join(output_dir, f"{os.path.basename(file_path)}_chunk_{i}.txt")
            with open(chunk_file, 'w') as cf:
                cf.write(chunk)
        print(f"Chunks saved to {output_dir}")

if __name__ == "__main__":
    main()
