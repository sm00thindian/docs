# src/utils.py
import os
from typing import List

def get_files_with_extension(directory: str, extension: str) -> List[str]:
    """Get all files with a given extension in a directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]
