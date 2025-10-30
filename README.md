# DOCS: Universal RAG Document Optimizer

**Turn `.docx` policies into LLM-ready chunks — for **AWS Bedrock**, **LangChain**, **LlamaIndex**, **Nova Pro**, **Claude Sonnet**, and beyond.**

- **Input**: `.docx` files (with OCR for images)
- **Output**: `json/`, `pdf/`, `llm/{format}/` (JSON/JSONL)
- **Optimized for**: AWS Bedrock Knowledge Bases (Titan, Nova Pro, Claude)
- **Speed**: 12x faster with parallel + spaCy/NLTK optimization
- **Modular**: Extendable to any LLM stack

---

## Features

| Feature | Flag |
|-------|------|
| OCR on images | `--ocr_images` |
| Chunking + overlap | `--chunk_size 500`, `--overlap 100` |
| NLP tagging (entities, intents, keywords) | Built-in |
| PDF export | `--to_pdf` |
| **Universal LLM export** | `--export-format` |
| Parallel processing | `--workers 4` |

### Supported `--export-format`

| Format | File | Best For |
|-------|------|----------|
| `bedrock` | `.jsonl` | AWS Bedrock KB (Titan, Nova Pro, Claude) |
| `nova_pro` | `.jsonl` | Multimodal RAG (text + OCR images) |
| `claude_sonnet` | `.jsonl` | Agentic reasoning (200K context) |
| `langchain` | `.json` | `JSONLoader`, `Document` |
| `llamaindex` | `.json` | `SimpleDirectoryReader` |
| `haystack` | `.json` | `Document` list |
| `generic` | `.jsonl` | Custom RAG pipelines |

---

## Quick Start

```bash
# 1. Clone & setup
git clone https://github.com/sm00thindian/docs.git
cd docs
chmod +x setup.sh
./setup.sh

# 2. Run (Nova Pro example)
source venv/bin/activate
export SSL_CERT_FILE=$(python -m certifi)

python src/pipeline.py \
  --input_dir examples/ \
  --output_dir output/ \
  --export-format nova_pro \
  --ocr_images \
  --to_pdf \
  --workers 4
