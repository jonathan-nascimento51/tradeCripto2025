import os
from typing import List

def extract_code_snippet(file_path: str, function_name: str, window: int = 30) -> str:
    """Return a slice of code around the specified function."""
    if not os.path.isfile(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if function_name in line:
            return "".join(lines[idx:idx + window])
    return ""

def extract_text_section(file_path: str, start_keyword: str, end_keyword: str) -> str:
    """Extract text between two keywords."""
    if not os.path.isfile(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if start == -1 and start_keyword in line:
            start = i
            continue
        if start != -1 and end_keyword in line:
            end = i
            break
    if start != -1 and end != -1:
        return "".join(lines[start:end])
    return ""

def get_file_structure(directory: str) -> List[str]:
    """Return a sorted list of file paths under the directory."""
    paths: List[str] = []
    for root_dir, _, files in os.walk(directory):
        for fname in files:
            rel = os.path.relpath(os.path.join(root_dir, fname), directory)
            paths.append(rel)
    return sorted(paths)