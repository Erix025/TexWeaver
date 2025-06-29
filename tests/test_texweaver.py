from pathlib import Path

import pytest

from texweaver import DefaultConfig, TexParser


def test_texweaver_basic():
    """Test basic TexWeaver functionality."""
    # Create a simple test markdown content
    test_content = """# Test Header

This is a test paragraph with **bold** and *italic* text.

## Subsection

- Item 1
- Item 2

Some `inline code` and a [link](https://example.com).
"""

    parser = TexParser()
    parser.parse(test_content)
    mdoc = parser.doc

    # Convert to LaTeX
    latex = mdoc.to_latex(DefaultConfig)

    # Basic assertions
    assert latex is not None
    assert len(latex) > 0
    assert "Test Header" in latex or "section" in latex.lower()


def test_texweaver_with_file():
    """Test TexWeaver with actual file if available."""
    # Look for test markdown files
    test_files = [
        Path("test.md"),
        Path("tests/test.md"),
        Path("../test.md"),
    ]

    test_file = None
    for file_path in test_files:
        if file_path.exists():
            test_file = file_path
            break

    if test_file:
        with open(test_file, "r", encoding="utf-8") as f:
            src = f.read()

        parser = TexParser()
        parser.parse(src)
        mdoc = parser.doc
        latex = mdoc.to_latex(DefaultConfig)

        assert latex is not None
        assert len(latex) > 0
    else:
        pytest.skip("No test markdown file found")


if __name__ == "__main__":
    test_texweaver_basic()
    test_texweaver_with_file()
