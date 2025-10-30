# DOCS: RAG Document Optimizer for AWS Bedrock

**Prepare .docx policies for AWS Bedrock Knowledge Bases — fast, clean, metadata-rich.**

- **Input**: `.docx` files (with OCR support)
- **Output**: `json/`, `pdf/`, `bedrock/*.jsonl`, `bedrock_corpus.jsonl`
- **Ready for**: `aws s3 cp` → Bedrock KB → Titan embeddings
- **Parallel**: 4–8x faster on multi-core
- **Modular**: Extendable for PDF, TXT, etc.

---

## Features

| Feature | Status |
|-------|--------|
| OCR on images | `--ocr_images` |
| Chunking + overlap | 500 words, 100 overlap |
| NLP tagging (spaCy + NLTK) | Entities, intents, keywords |
| Bedrock JSONL | `--to_bedrock` |
| PDF export | `--to_pdf` |
| Parallel processing | `--workers` |

---

## Quick Start

```bash
# 1. Setup
chmod +x setup.sh
./setup.sh

# 2. Run
source venv/bin/activate
export SSL_CERT_FILE=$(python -m certifi)

python src/pipeline.py \
  --input_dir examples/ \
  --output_dir output/ \
  --to_bedrock \
  --ocr_images \
  --workers 4
