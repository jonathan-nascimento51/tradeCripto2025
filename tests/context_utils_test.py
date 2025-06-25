import os
import sys

try:
    from tools import context_utils as cu
except ImportError:  # Allow direct execution without PYTHONPATH tweaks
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from tools import context_utils as cu

if __name__ == "__main__":
    # Display the first few files inside the libraries directory
    print("Sample files:", cu.get_file_structure("libraries")[:3])

    # Extract a snippet from the confluence library
    snippet = cu.extract_code_snippet(
        "libraries/confluence_lib.pine", "calculateConfluence"
    )
    print(
        "Snippet start:",
        snippet.splitlines()[0] if snippet else "not found",
    )

    # Extract a README section
    text = cu.extract_text_section(
        "README.md", "## Helper Libraries", "## Using the Libraries"
    )
    print("Section lines:", len(text.splitlines()))
