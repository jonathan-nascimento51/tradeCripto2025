import os
import sys

try:
    from tools import context_utils as cu
except ImportError:  # Allow direct execution without PYTHONPATH tweaks
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from tools import context_utils as cu


def test_context_utils_basic() -> None:
    """Validate a couple helper functions return expected output."""

    # Should list at least one file under libraries/
    sample_files = cu.get_file_structure("libraries")
    assert len(sample_files) > 0

    # Snippet extraction should include the requested function name
    snippet = cu.extract_code_snippet(
        "libraries/confluence_lib.pine", "calculateConfluence"
    )
    assert "calculateConfluence" in snippet

    # Documentation section between two headings should not be empty
    text = cu.extract_text_section(
        "README.md", "## Helper Libraries", "## Context Utilities"
    )
    assert len(text.splitlines()) > 0
