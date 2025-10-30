# src/bedrock_export.py
import json
import os
from typing import List, Dict
from datetime import datetime


def export_to_bedrock_jsonl(
    tagged_chunks: List[Dict],
    output_file: str,
    source_name: str = "DOCS Pipeline"
) -> str:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in tagged_chunks:
            bedrock_entry = {
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
            # Clean empty
            bedrock_entry["metadata"] = {
                k: v for k, v in bedrock_entry["metadata"].items()
                if v not in ([], {}, None, "")
            }
            f.write(json.dumps(bedrock_entry, ensure_ascii=False) + "\n")
    
    return output_file
