# src/utils.py

import os
from typing import List

def find_documents(directory: str, extension: str) -> List[str]:
    """
    Recursively finds files with the given extension.
    """
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extension):
                matching_files.append(os.path.join(root, file))
    return matching_files
