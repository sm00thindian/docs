import os
import json
import argparse
from ingestion import WordDocumentIngester
from cleaning import TextCleaner
from chunking import TextChunker
from tagging import TextTagger
from utils import get_files_with_extension
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def process_document(file_path: str, output_dir: str, chunk_size: int, overlap: int, to_pdf: bool) -> None:
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
    output_json_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(tagged_chunks, f, indent=4, ensure_ascii=False)
    
    print(f"Processed {file_path} -> {output_json_file}")
    
    # Optional: Convert JSON to PDF
    if to_pdf:
        output_pdf_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.pdf")
        json_to_pdf(output_json_file, output_pdf_file)
        print(f"Converted {output_json_file} -> {output_pdf_file}")
    
    # Future: Add more steps here (e.g., embedding)

def json_to_pdf(json_file: str, pdf_file: str) -> None:
    """Convert a JSON file with tagged chunks to a PDF."""
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    # Set up PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    story.append(Paragraph(f"Document Analysis: {chunks[0]['file_name']}", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Add each chunk
    for chunk in chunks:
        story.append(Paragraph(f"Chunk {chunk['chunk_id']}", styles['Heading2']))
        story.append(Paragraph(f"Content: {chunk['content']}", styles['BodyText']))
        story.append(Paragraph(f"Word Count: {chunk['word_count']}", styles['BodyText']))
        story.append(Paragraph(f"Keywords: {', '.join(chunk['keywords'])}", styles['BodyText']))
        story.append(Paragraph(f"Entities: {', '.join([f'{ent[0]} ({ent[1]})' for ent in chunk['entities']])}", styles['BodyText']))
        story.append(Paragraph(f"Policy Keywords: {', '.join(chunk['policy_keywords'])}", styles['BodyText']))
        story.append(Paragraph(f"Intents: {', '.join(chunk['intents'])}", styles['BodyText']))
        story.append(Paragraph(f"Chunk Position: {chunk['chunk_position']:.2f}", styles['BodyText']))
        if 'error' in chunk:
            story.append(Paragraph(f"Error: {chunk['error']}", styles['BodyText']))
        story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Document Optimizer Pipeline")
    parser.add_argument("--input_dir", required=True, help="Directory with input documents")
    parser.add_argument("--output_dir", default="output", help="Output directory")
    parser.add_argument("--chunk_size", type=int, default=500, help="Chunk size in words")
    parser.add_argument("--overlap", type=int, default=100, help="Overlap in words")
    parser.add_argument("--to_pdf", action="store_true", help="Convert JSON outputs to PDF")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Process all .docx files
    docx_files = get_files_with_extension(args.input_dir, '.docx')
    for file_path in docx_files:
        process_document(file_path, args.output_dir, args.chunk_size, args.overlap, args.to_pdf)
