# src/main.py
import json
from src.word_optimizer import WordDocumentOptimizer
from src.utils import find_documents
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.json')
    absolute_path = os.path.abspath(config_path)
    print(f"Script dir: {script_dir}")
    print(f"Config path (joined): {config_path}")
    print(f"Absolute config path: {absolute_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    input_dir = config['directories']['input']
    
    optimizer = WordDocumentOptimizer()
    files = find_documents(input_dir, optimizer.file_extension)
    
    for file_path in files:
        print(f"Processing {file_path}")
        content = optimizer.load_document(file_path)
        chunks = optimizer.optimize(content)
        print(f"Optimized into {len(chunks)} chunks.")

if __name__ == "__main__":
    main()
