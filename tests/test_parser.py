from pathlib import Path

import pytest

from texweaver import TexParser


def test_parser_basic():
    """Test basic parser functionality."""
    # Create a simple test markdown content
    test_content = """# Test Header

This is a test paragraph.

- Item 1
- Item 2
"""

    parser = TexParser()
    parser.parse(test_content)

    # Basic assertion to ensure parser works
    assert parser.doc is not None

    # Convert to JSON and check structure
    json_output = parser.doc.to_json()
    assert json_output is not None


def test_parser_with_file():
    """Test parser with actual file if available."""
    # Look for test markdown files in the current directory or tests directory
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

        assert parser.doc is not None
        json_output = parser.doc.to_json()
        assert json_output is not None
    else:
        pytest.skip("No test markdown file found")


if __name__ == "__main__":
    test_parser_basic()
    test_parser_with_file()
