# DOCS: Universal RAG Document Optimizer

Turn `.docx` policies into LLM-ready chunks — for **AWS Bedrock**, **LangChain**, **LlamaIndex**, **Nova Pro**, **Claude Sonnet**, and beyond.

- **Input**: `.docx` files (with OCR for images)
- **Output**: `json/`, `pdf/`, `llm/{format}/` (JSON/JSONL)
- **Optimized for**: AWS Bedrock Knowledge Bases (Titan, Nova Pro, Claude)
- **Speed**: faster with parallel + spaCy/NLTK optimization
- **Modular**: Extendable to any LLM stack

---

[TOC]

## Features

| Feature | Flag |
|---|---|
| OCR on images | `--ocr_images` |
| Chunking + overlap | `--chunk_size 500`, `--overlap 100` |
| NLP tagging (entities, intents, keywords) | Built-in |
| PDF export | `--to_pdf` |
| Universal LLM export | `--export-format` |
| Parallel processing | `--workers 4` |

### Supported `--export-format`

| Format | File | Best For |
|---|---|---|
| `bedrock` | `.jsonl` | AWS Bedrock KB (Titan, Nova Pro, Claude) |
| `nova_pro` | `.jsonl` | Multimodal RAG (text + OCR images) |
| `claude_sonnet` | `.jsonl` | Agentic reasoning (200K context) |
| `langchain` | `.json` | `JSONLoader`, `Document` |
| `llamaindex` | `.json` | `SimpleDirectoryReader` |
| `haystack` | `.json` | `Document` list |
| `generic` | `.jsonl` | Custom RAG pipelines |

---

## Prerequisites

- Python 3.9 or newer
- git, pip
- Recommended: use a virtual environment

## Installation

```bash
git clone https://github.com/sm00thindian/docs.git
cd docs
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Install spaCy language model (if not included in requirements):
# python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.1/en_core_web_lg-3.7.1-py3-none-any.whl
# or
# python -m spacy download en_core_web_lg
```

If you encounter SSL certificate issues on macOS, set:

```bash
export SSL_CERT_FILE=$(python -m certifi)
```

## Quick Start

Run a pipeline (Nova Pro example):

```bash
source venv/bin/activate
python src/pipeline.py \
  --input_dir examples/ \
  --output_dir output/ \
  --export-format nova_pro \
  --ocr_images \
  --to_pdf \
  --workers 4
```

Notes:
- `--input_dir`: path to `.docx` files
- `--output_dir`: default `output`
- `--export-format`: choices: bedrock, nova_pro, claude_sonnet, langchain, llamaindex, haystack, generic

## Configuration

Place `config.yaml` in the repository root (or pass equivalent flags). CLI flags override values in `config.yaml`.

Example `config.yaml`:

```yaml
chunk_size: 500
overlap: 100
ocr_images: false
to_pdf: false
workers: 4
```

## Examples & Output

Example output structure:

```
output/
├── json/                  ← Debug (always)
│   └── Policy1.json
├── pdf/                   ← Optional
│   └── Policy1.pdf
├── llm/
│   ├── claude_sonnet/
│   │   ├── Policy1.jsonl
│   │   └── Policy2.jsonl
│   └── nova_pro/
└── claude_sonnet_corpus.jsonl  ← Upload to S3
```

Sample (bedrock) JSONL document entry:

```json
{"id": "policy-1-0001", "text": "...chunk text...", "metadata": {"source": "Policy1.docx", "page": 3}}
```

## CLI Reference

```bash
python src/pipeline.py --help

--input_dir       Required: Path to .docx files
--output_dir      Default: output
--chunk_size      Default: 500
--overlap         Default: 100
--ocr_images      Enable OCR on images
--to_pdf          Generate PDFs
--export-format   Choices: bedrock, nova_pro, claude_sonnet, langchain, llamaindex, haystack, generic
                  Default: bedrock
--workers         Default: 4 (auto-detect)
```

## Contributing

Contributions welcome. Please open issues or pull requests. Add tests for new features and follow existing code style. Maintain a short changelog for user-facing changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact / Maintainers

Maintained by @sm00thindian. Open issues for feature requests or bugs.

---