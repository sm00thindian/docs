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
from llm_export import (
    export_langchain, export_llamaindex, export_haystack,
    export_generic_jsonl, export_bedrock_jsonl,
    export_nova_pro, export_claude_sonnet
)
from multiprocessing import Pool, cpu_count
from functools import partial


def process_single(
    file_path: str,
    output_dir: str,
    chunk_size: int,
    overlap: int,
    ocr_images: bool,
    to_pdf: bool,
    export_format: str,
) -> dict:
    """
    Process a single .docx file.
    Returns a dict with paths to the generated files.
    """
    try:
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]

        # ------------------------------------------------------------------
        # Core pipeline
        # ------------------------------------------------------------------
        raw_text = WordDocumentIngester().ingest(file_path, ocr_images=ocr_images)
        cleaned_text = TextCleaner().clean(raw_text)
        chunks = TextChunker(chunk_size=chunk_size, overlap=overlap).chunk(cleaned_text)
        tagged_chunks = TextTagger().tag_chunks(chunks, file_name)

        # ------------------------------------------------------------------
        # Output directories
        # ------------------------------------------------------------------
        json_dir = os.path.join(output_dir, "json")
        pdf_dir  = os.path.join(output_dir, "pdf")
        llm_dir  = os.path.join(output_dir, "llm", export_format)

        # JSON (always – for debugging)
        os.makedirs(json_dir, exist_ok=True)
        json_file = os.path.join(json_dir, f"{base_name}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(tagged_chunks, f, indent=4, ensure_ascii=False)

        # PDF (optional)
        pdf_file = None
        if to_pdf:
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_file = os.path.join(pdf_dir, f"{base_name}.pdf")
            PDFConverter().convert(json_file, pdf_file)

        # LLM export (the heart of the pipeline)
        llm_file = None
        ext = "jsonl" if export_format in ("bedrock", "generic", "nova_pro", "claude_sonnet") else "json"
        llm_path = os.path.join(llm_dir, f"{base_name}.{ext}")
        os.makedirs(llm_dir, exist_ok=True)

        if export_format == "bedrock":
            export_bedrock_jsonl(tagged_chunks, llm_path, source_name=file_name)
        elif export_format == "langchain":
            export_langchain(tagged_chunks, llm_path, source_name=file_name)
        elif export_format == "llamaindex":
            export_llamaindex(tagged_chunks, llm_path, source_name=file_name)
        elif export_format == "haystack":
            export_haystack(tagged_chunks, llm_path, source_name=file_name)
        elif export_format == "generic":
            export_generic_jsonl(tagged_chunks, llm_path, source_name=file_name)
        elif export_format == "nova_pro":
            export_nova_pro(tagged_chunks, llm_path, source_name=file_name)
        elif export_format == "claude_sonnet":
            export_claude_sonnet(tagged_chunks, llm_path, source_name=file_name)

        llm_file = llm_path

        print(f"Done: {file_name} ({export_format})")
        return {"json": json_file, "pdf": pdf_file, "llm": llm_file}

    except Exception as e:
        print(f"Failed {file_path}: {e}")
        return {"json": None, "pdf": None, "llm": None}


# ----------------------------------------------------------------------
# CLI entry point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Universal RAG Document Optimizer"
    )
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", default="output")
    parser.add_argument("--chunk_size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument("--ocr_images", action="store_true")
    parser.add_argument("--to_pdf", action="store_true")
    parser.add_argument(
        "--export-format",
        choices=[
            "bedrock", "langchain", "llamaindex", "haystack",
            "generic", "nova_pro", "claude_sonnet"
        ],
        default="bedrock",
    )
    parser.add_argument("--workers", type=int, default=min(4, cpu_count()))

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    docx_files = get_files_with_extension(args.input_dir, ".docx")
    if not docx_files:
        print("No .docx files found.")
        exit(0)

    # ------------------------------------------------------------------
    # Build a callable that already knows the shared arguments
    # ------------------------------------------------------------------
    worker = partial(
        process_single,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        ocr_images=args.ocr_images,
        to_pdf=args.to_pdf,
        export_format=args.export_format,
    )

    # ------------------------------------------------------------------
    # Parallel execution
    # ------------------------------------------------------------------
    with Pool(args.workers) as pool:
        results = pool.map(worker, docx_files)

    # ------------------------------------------------------------------
    # Combine JSONL corpora (bedrock, generic, nova_pro, claude_sonnet)
    # ------------------------------------------------------------------
    if args.export_format in ("bedrock", "generic", "nova_pro", "claude_sonnet"):
        combined_path = os.path.join(args.output_dir, f"{args.export_format}_corpus.jsonl")
        with open(combined_path, "w", encoding="utf-8") as out_f:
            for res in results:
                if res["llm"]:
                    with open(res["llm"], "r", encoding="utf-8") as in_f:
                        out_f.write(in_f.read())
        print(f"Combined {args.export_format} corpus: {combined_path}")

    print(f"Processed {len(docx_files)} files to {args.output_dir}")
