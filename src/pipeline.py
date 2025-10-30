# src/pipeline.py
import os
import json
import argparse
from ingestion import WordDocumentIngester
from cleaning import TextCleaner
from chunking import TextChunker
from tagging import TextTagger
from utils import get_files_with_extension
from pdf_conversion import PDFConverter  # Reuse fixed class


def process_document(file_path: str, output_dir: str, chunk_size: int, overlap: int, ocr_images: bool, to_pdf: bool) -> None:
    file_name = os.path.basename(file_path)
    
    # Step 1–4
    raw_text = WordDocumentIngester().ingest(file_path, ocr_images=ocr_images)
    cleaned_text = TextCleaner().clean(raw_text)
    chunks = TextChunker(chunk_size=chunk_size, overlap=overlap).chunk(cleaned_text)
    tagged_chunks = TextTagger().tag_chunks(chunks, file_name)
    
    # Output JSON
    output_json_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(tagged_chunks, f, indent=4, ensure_ascii=False)
    print(f"Processed {file_path} → {output_json_file}")
    
    # Optional PDF
    if to_pdf:
        output_pdf_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.pdf")
        PDFConverter().convert(output_json_file, output_pdf_file)
        print(f"Converted {output_json_file} → {output_pdf_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Document Optimizer Pipeline")
    parser.add_argument("--input_dir", required=True, help="Directory with input documents")
    parser.add_argument("--output_dir", default="output", help="Output directory")
    parser.add_argument("--chunk_size", type=int, default=500, help="Chunk size in words")
    parser.add_argument("--overlap", type=int, default=100, help="Overlap in words")
    parser.add_argument("--ocr_images", action="store_true", help="Enable OCR on images")
    parser.add_argument("--to_pdf", action="store_true", help="Convert JSON to PDF")
    
    args = parser.parse_args()
    
    docx_files = get_files_with_extension(args.input_dir, '.docx')
    for file_path in docx_files:
        process_document(file_path, args.output_dir, args.chunk_size, args.overlap, args.ocr_images, args.to_pdf)
