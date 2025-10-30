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
from bedrock_export import export_to_bedrock_jsonl
from multiprocessing import Pool, cpu_count
from functools import partial


def process_single(args):
    (
        file_path, output_dir, chunk_size, overlap,
        ocr_images, to_pdf, to_bedrock
    ) = args
    try:
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]

        # Core pipeline
        ingester = WordDocumentIngester()
        cleaner = TextCleaner()
        chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
        tagger = TextTagger()

        raw_text = ingester.ingest(file_path, ocr_images=ocr_images)
        cleaned_text = cleaner.clean(raw_text)
        chunks = chunker.chunk(cleaned_text)
        tagged_chunks = tagger.tag_chunks(chunks, file_name)

        # Define subdirs
        json_dir = os.path.join(output_dir, "json")
        pdf_dir = os.path.join(output_dir, "pdf")
        bedrock_dir = os.path.join(output_dir, "bedrock")

        # Always create json dir
        os.makedirs(json_dir, exist_ok=True)
        json_file = os.path.join(json_dir, f"{base_name}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(tagged_chunks, f, indent=4, ensure_ascii=False)

        # Optional: PDF
        if to_pdf:
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_file = os.path.join(pdf_dir, f"{base_name}.pdf")
            PDFConverter().convert(json_file, pdf_file)

        # Optional: Bedrock JSONL
        bedrock_file = None
        if to_bedrock:
            os.makedirs(bedrock_dir, exist_ok=True)
            bedrock_file = os.path.join(bedrock_dir, f"{base_name}.jsonl")
            export_to_bedrock_jsonl(tagged_chunks, bedrock_file, source_name=file_name)

        print(f"Done: {file_name}")
        return {
            "json": json_file,
            "pdf": pdf_file if to_pdf else None,
            "bedrock": bedrock_file
        }
    except Exception as e:
        print(f"Failed {file_path}: {e}")
        return {"json": None, "pdf": None, "bedrock": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS Bedrock RAG Document Optimizer")
    parser.add_argument("--input_dir", required=True, help="Input .docx directory")
    parser.add_argument("--output_dir", default="output", help="Root output directory")
    parser.add_argument("--chunk_size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument("--ocr_images", action="store_true")
    parser.add_argument("--to_pdf", action="store_true", help="Generate PDFs")
    parser.add_argument("--to_bedrock", action="store_true", help="Generate Bedrock JSONL")
    parser.add_argument("--workers", type=int, default=min(4, cpu_count()))

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    docx_files = get_files_with_extension(args.input_dir, '.docx')
    if not docx_files:
        print("No .docx files found.")
        exit(0)

    process_func = partial(
        process_single,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        ocr_images=args.ocr_images,
        to_pdf=args.to_pdf,
        to_bedrock=args.to_bedrock
    )

    with Pool(args.workers) as pool:
        results = pool.map(process_func, docx_files)

    # Combine Bedrock JSONL if enabled
    if args.to_bedrock:
        combined_file = os.path.join(args.output_dir, "bedrock_corpus.jsonl")
        with open(combined_file, 'w', encoding='utf-8') as outfile:
            for res in results:
                if res["bedrock"]:
                    with open(res["bedrock"], 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
        print(f"Combined Bedrock corpus: {combined_file}")

    print(f"Processed {len(docx_files)} files → {args.output_dir}")
