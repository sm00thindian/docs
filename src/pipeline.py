# src/pipeline.py
import os
import json
import argparse
from ingestion import WordDocumentIngester
from cleaning import TextCleaner
from chunking import TextChunker
from tagging import TextTagger
from utils import get_files_with_extension

def process_document(file_path: str, output_dir: str, chunk_size: int, overlap: int) -> None:
    """Full pipeline for a single document."""
    file_name = os.path.basename(file_path)
    
    # Step 1: Ingestion
    ingester = WordDocumentIngester()  # Easy to swap for other ingesters
    raw_text = ingester.ingest(file_path)
    
    # Step 2: Cleaning
    cleaner = TextCleaner()
    cleaned_text = cleaner.clean(raw_text)
    
    # Step 3: Chunking
    chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
    chunks = chunker.chunk(cleaned_text)
    
    # Step 4: Tagging
    tagger = TextTagger()
    tagged_chunks = tagger.tag_chunks(chunks, file_name)
    
    # Output to JSON
    output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tagged_chunks, f, indent=4, ensure_ascii=False)
    
    print(f"Processed {file_path} -> {output_file}")
    
    # Future: Add more steps here (e.g., embedding)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Document Optimizer Pipeline")
    parser.add_argument("--input_dir", required=True, help="Directory with input documents")
    parser.add_argument("--output_dir", default="output", help="Output directory")
    parser.add_argument("--chunk_size", type=int, default=500, help="Chunk size in words")
    parser.add_argument("--overlap", type=int, default=100, help="Overlap in words")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Process all .docx files (extensible to other extensions)
    docx_files = get_files_with_extension(args.input_dir, '.docx')
    for file_path in docx_files:
        process_document(file_path, args.output_dir, args.chunk_size, args.overlap)
