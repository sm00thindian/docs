# src/main.py

import yaml
from .word_optimizer import WordDocumentOptimizer
from .utils import find_documents
import os  # Added for path handling

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, '..', 'config.yaml')
print(f"Looking for config at: {config_path}")  # Debug line
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

def main():
    # Calculate project root: parent of src/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.yaml')  # Changed to go up one level
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    input_dir = config['directories']['input']
    
    # Example: Use Word optimizer
    optimizer = WordDocumentOptimizer()  # Will use dynamic path internally
    files = find_documents(input_dir, optimizer.file_extension)
    
    for file_path in files:
        print(f"Processing {file_path}")
        content = optimizer.load_document(file_path)
        chunks = optimizer.optimize(content)
        print(f"Optimized into {len(chunks)} chunks.")
        # Optionally save chunks to output dir, e.g., write to files
    
if __name__ == "__main__":
    main()