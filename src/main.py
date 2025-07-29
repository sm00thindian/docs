# src/main.py

import os  # For path handling
import sys
import json

# Add project root to sys.path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.word_optimizer import WordDocumentOptimizer
from src.utils import find_documents

def main():
    # Calculate project root: parent of src/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.json')
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    input_dir = config['directories']['input']
    output_dir = config['directories']['output']
    removed_dir = config['directories']['removed']
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(removed_dir, exist_ok=True)
    
    # Example: Use Word optimizer
    optimizer = WordDocumentOptimizer()
    files = find_documents(input_dir, optimizer.file_extension)
    
    for file_path in files:
        print(f"Processing {file_path}")
        content = optimizer.load_document(file_path)
        if content is None:
            continue
        chunks = optimizer.optimize(content)
        print(f"Optimized into {len(chunks)} chunks.")
        
        # Save optimized chunks as JSON with metadata
        chunks_file = os.path.join(output_dir, f"{os.path.basename(file_path)}_chunks.json")
        with open(chunks_file, 'w') as cf:
            json.dump(chunks, cf, indent=4)
        print(f"Chunks saved to {chunks_file}")

        # Extract and save removed sections
        removed_chunks = optimizer.extract_removed(content)
        if removed_chunks:
            for i, chunk in enumerate(removed_chunks, 1):
                removed_file = os.path.join(removed_dir, f"{os.path.basename(file_path)}_removed_{i}.txt")
                with open(removed_file, 'w') as rf:
                    rf.write(chunk)
            print(f"Removed sections saved to {removed_dir}")
        else:
            print(f"No removed sections for {file_path}")

if __name__ == "__main__":
    main()
