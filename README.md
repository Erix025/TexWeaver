# TexWeaver

A powerful and flexible Markdown to LaTeX converter with support for multiple customizable templates.

## Features

- **Multiple Templates**: Choose from built-in templates (default, presentation) or create custom ones
- **Flexible Configuration**: Easy-to-edit YAML configuration files with multi-line text support
- **Rich Formatting**: Support for text formatting, math formulas, lists, code blocks, and images
- **Modern Development**: Built with uv for fast dependency management

## Installation

### Using uv (recommended)

```bash
uv add texweaver
```

### Using pip

```bash
pip install texweaver
```

## Usage

### Basic Usage

```bash
# Use default template
texweaver input.md output.tex

# Use specific template
texweaver -t presentation input.md output.tex
```

### Available Templates

```bash
# List all available templates
texweaver --list-templates

# Get information about a specific template
texweaver --template-info presentation
```

Built-in templates:

- **default**: Standard LaTeX document template
- **presentation**: Beamer template for presentations

### Custom Configuration

```bash
# Use custom configuration file
texweaver -c my-template.yaml input.md output.tex
```

### Advanced Usage Examples

```bash

# Presentation slides
texweaver -t presentation slides.md presentation.tex
```

## Template System

TexWeaver uses a flexible YAML-based template system that supports:

- **Multi-line templates**: Use YAML's `|` syntax for complex LaTeX structures
- **Categorized rules**: Organize templates by category (formatting, math, lists, etc.)
- **Variable substitution**: Dynamic content insertion with `{variable}` syntax
- **Hierarchical configuration**: Override specific rules while inheriting others

### Creating Custom Templates

Create a YAML file with the following structure:

```yaml
name: "My Custom Template"
description: "Description of the template"
author: "Your Name"
version: "1.0"

# Document structure
document:
  preamble: |
    \documentclass{article}
    \usepackage{custom-package}

# Text formatting
formatting:
  heading1: |
    \section{{{content}}}

  bold: "\\textbf{{{content}}}"

# Math formulas
math:
  inline_formula: "${content}$"
# And more categories...
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Setup development environment

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/erix025/texweaver
cd texweaver

# Create virtual environment and install dependencies
uv sync --all-extras
```

### Running tests

```bash
uv run pytest
```

### Code formatting

```bash
uv run black src tests
uv run isort src tests
```

### Type checking

```bash
uv run mypy src
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
