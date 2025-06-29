# TexWeaver

A simple converter from Markdown to LaTeX.

## Installation

### Using uv (recommended)

```bash
uv add texweaver
```

### Using pip

```bash
pip install texweaver
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

# Activate the virtual environment
source .venv/bin/activate
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

## Usage

### With activated virtual environment

```bash
source .venv/bin/activate
texweaver input.md output.tex
```

### With uv run (recommended)

```bash
uv run texweaver input.md output.tex
```

### Direct execution

```bash
.venv/bin/texweaver input.md output.tex
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
