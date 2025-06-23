import os
from typing import List

def extract_code_snippet(file_path: str, function_name: str, window: int = 30) -> str:
    """Return `window` lines after the first match of `function_name`.
    file_path: path to the source file.
    function_name: name of the function to locate.
    window: how many lines to keep after the match.
    Returns the extracted snippet or an empty string.
    Example: extract_code_snippet('mod.py', 'main', 10)
    """
    if not os.path.isfile(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if function_name in line:
            return "".join(lines[idx:idx + window])
    return ""

def extract_text_section(file_path: str, start_keyword: str, end_keyword: str) -> str:
    """Return text located between `start_keyword` and `end_keyword`.
    file_path: file to search.
    start_keyword: text marking start of the section.
    end_keyword: text marking its end.
    Returns the captured text or an empty string.
    Example: extract_text_section('README.md', '# Start', '# End')
    """
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
    """Return sorted relative file paths found under `directory`.
    directory: root folder to scan.
    Returns a list of paths sorted alphabetically.
    Example: get_file_structure('tests')[:2]
    """
    paths: List[str] = []
    for root_dir, _, files in os.walk(directory):
        for fname in files:
            rel = os.path.relpath(os.path.join(root_dir, fname), directory)
            paths.append(rel)
    return sorted(paths)
