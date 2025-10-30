# src/pipeline.py
import os
import json
import argparse
from ingestion import WordDocumentIngester
from cleaning import TextCleaner
from chunking import TextChunker
from tagging import TextTagger
from utils import get_files_with_extension
from pdf_conversion import PDFConverter
from multiprocessing import Pool, cpu_count
from functools import partial

def process_single(args):
    file_path, output_dir, chunk_size, overlap, ocr_images, to_pdf = args
    try:
        file_name = os.path.basename(file_path)
        ingester = WordDocumentIngester()
        cleaner = TextCleaner()
        chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
        tagger = TextTagger()

        raw_text = ingester.ingest(file_path, ocr_images=ocr_images)
        cleaned_text = cleaner.clean(raw_text)
        chunks = chunker.chunk(cleaned_text)
        tagged_chunks = tagger.tag_chunks(chunks, file_name)

        os.makedirs(output_dir, exist_ok=True)
        json_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(tagged_chunks, f, indent=4, ensure_ascii=False)

        if to_pdf:
            pdf_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.pdf")
            PDFConverter().convert(json_file, pdf_file)

        print(f"Done: {file_name}")
        return json_file
    except Exception as e:
        print(f"Failed {file_path}: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel RAG Document Optimizer")
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", default="output")
    parser.add_argument("--chunk_size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument("--ocr_images", action="store_true")
    parser.add_argument("--to_pdf", action="store_true")
    parser.add_argument("--workers", type=int, default=min(4, cpu_count()), help="Parallel workers")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    docx_files = get_files_with_extension(args.input_dir, '.docx')
    if not docx_files:
        print("No .docx files found.")
        exit(0)

    # Parallel file processing
    process_func = partial(
        process_single,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        ocr_images=args.ocr_images,
        to_pdf=args.to_pdf
    )
    with Pool(args.workers) as pool:
        list(pool.map(process_func, docx_files))

    print(f"Processed {len(docx_files)} files → {args.output_dir}")
