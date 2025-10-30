# src/llm_export.py
import json
import os
from typing import List, Dict
from datetime import datetime


# ----------------------------------------------------------------------
#  Existing exporters (unchanged – kept for completeness)
# ----------------------------------------------------------------------
def export_langchain(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str
) -> str:
    """LangChain: List of {'page_content': str, 'metadata': dict}"""
    docs = [
        {
            "page_content": chunk["content"],
            "metadata": {
                "source": f"{source_name}#chunk-{chunk['chunk_id']}",
                "chunk_id": chunk["chunk_id"],
                "file_name": chunk["file_name"],
                "chunk_position": chunk["chunk_position"],
                **{k: v for k, v in chunk.items()
                   if k not in ["content", "chunk_id", "file_name", "chunk_position"]}
            }
        }
        for chunk in tagged_chunks
    ]
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
    return output_file


def export_llamaindex(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str
) -> str:
    """LlamaIndex: Flat metadata with tags"""
    docs = [
        {
            "text": chunk["content"],
            "metadata": {
                "file_name": chunk["file_name"],
                "chunk_id": chunk["chunk_id"],
                "source": source_name,
                "ingestion_time": datetime.utcnow().isoformat() + "Z",
                "tags": chunk["keywords"] + chunk["policy_keywords"] + chunk["intents"]
            }
        }
        for chunk in tagged_chunks
    ]
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
    return output_file


def export_haystack(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str
) -> str:
    """Haystack: {'content': str, 'meta': dict}"""
    docs = [
        {
            "content": chunk["content"],
            "meta": {
                "name": f"{source_name}_chunk_{chunk['chunk_id']}",
                "file_name": chunk["file_name"],
                "chunk_id": chunk["chunk_id"],
                "intents": chunk["intents"],
                "entities": [e[0] for e in chunk["entities"]],
                "keywords": chunk["keywords"]
            }
        }
        for chunk in tagged_chunks
    ]
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
    return output_file


def export_generic_jsonl(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str
) -> str:
    """Simple flat JSONL"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in tagged_chunks:
            flat = {
                "id": f"{source_name.replace('.docx', '')}_{chunk['chunk_id']}",
                "text": chunk["content"],
                "source": source_name,
                "chunk_id": chunk["chunk_id"],
                "keywords": "|".join(chunk["keywords"]),
                "intents": "|".join(chunk["intents"]),
                "entities": "|".join([e[0] for e in chunk["entities"]])
            }
            f.write(json.dumps(flat, ensure_ascii=False) + "\n")
    return output_file


def export_bedrock_jsonl(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str
) -> str:
    """Standard Bedrock JSONL"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in tagged_chunks:
            entry = {
                "text": chunk["content"],
                "metadata": {
                    "source": source_name,
                    "file_name": chunk["file_name"],
                    "chunk_id": chunk["chunk_id"],
                    "chunk_position": round(chunk["chunk_position"], 3),
                    "word_count": chunk["word_count"],
                    "keywords": chunk["keywords"],
                    "policy_keywords": chunk["policy_keywords"],
                    "intents": chunk["intents"],
                    "entities": chunk["entities"],
                    "ingestion_timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
            entry["metadata"] = {
                k: v for k, v in entry["metadata"].items()
                if v not in ([], {}, None, "")
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return output_file


# ----------------------------------------------------------------------
#  Fixed exporters (Nova Pro & Claude Sonnet)
# ----------------------------------------------------------------------
def export_nova_pro(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str
) -> str:
    """Nova Pro – adds multimodal fields"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in tagged_chunks:
            # ---- compute multimodal_type before the dict ----
            has_image = "[Image" in chunk["content"]
            multimodal_type = "text/image" if has_image else "text"

            entry = {
                "text": chunk["content"],
                "metadata": {
                    "source": source_name,
                    "file_name": chunk["file_name"],
                    "chunk_id": chunk["chunk_id"],
                    "chunk_position": round(chunk["chunk_position"], 3),
                    "word_count": chunk["word_count"],
                    "keywords": chunk["keywords"],
                    "policy_keywords": chunk["policy_keywords"],
                    "intents": chunk["intents"],
                    "entities": chunk["entities"],
                    "ingestion_timestamp": datetime.utcnow().isoformat() + "Z",
                    # Nova Pro custom fields
                    "multimodal_type": multimodal_type,
                    "content_modality": "structured"
                }
            }
            # prune empty values
            entry["metadata"] = {
                k: v for k, v in entry["metadata"].items()
                if v not in ([], {}, None, "")
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return output_file


def export_claude_sonnet(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str
) -> str:
    """Claude Sonnet – adds reasoning hints"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in tagged_chunks:
            # ---- compute reasoning hint before the dict ----
            reasoning_hint = (
                ["multi-step"] if "procedure" in chunk["intents"] else ["contextual"]
            )

            entry = {
                "text": chunk["content"],
                "metadata": {
                    "source": source_name,
                    "file_name": chunk["file_name"],
                    "chunk_id": chunk["chunk_id"],
                    "chunk_position": round(chunk["chunk_position"], 3),
                    "word_count": chunk["word_count"],
                    "keywords": chunk["keywords"],
                    "policy_keywords": chunk["policy_keywords"],
                    "intents": chunk["intents"],
                    "entities": chunk["entities"],
                    "ingestion_timestamp": datetime.utcnow().isoformat() + "Z",
                    # Claude Sonnet custom fields
                    "reasoning_hints": reasoning_hint,
                    "contextual_tags": [e[0] for e in chunk["entities"]] + chunk["policy_keywords"]
                }
            }
            entry["metadata"] = {
                k: v for k, v in entry["metadata"].items()
                if v not in ([], {}, None, "")
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return output_file
