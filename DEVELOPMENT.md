# Development Guide

## Project Structure

```
TexWeaver/
├── src/
│   └── texweaver/          # Main source code
├── tests/                  # Test files
├── .vscode/                # VS Code configuration
├── pyproject.toml          # Project configuration and dependencies
├── uv.lock                 # Locked dependency versions
├── README.md               # Project documentation
└── LICENSE                 # License
```

## Setting Up the Development Environment

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Set Up the Development Environment

```bash
# Clone the repository
git clone https://github.com/erix025/texweaver
cd texweaver

# Create a virtual environment and install dependencies
uv sync --all-extras

# Activate the virtual environment
source .venv/bin/activate
```

## Common Commands

### Install Dependencies

```bash
uv sync --all-extras
```

### Run Tests

```bash
uv run pytest                    # Basic tests
uv run pytest --cov              # Tests with coverage
uv run pytest -v                 # Verbose output
```

### Code Quality Checks

```bash
uv run black src tests           # Code formatting
uv run isort src tests           # Import sorting
uv run flake8 src tests          # Linting
uv run mypy src                  # Type checking
```

### Build the Project

```bash
uv build                         # Build distribution package
```

### Install Local Development Version

```bash
uv add -e .                      # Install in editable mode
```

## VS Code Tasks

The project is configured with the following VS Code tasks (access via Ctrl+Shift+P -> Tasks: Run Task):

- **Install Dependencies**: Install all dependencies
- **Run Tests**: Run tests
- **Run Tests with Coverage**: Run tests with coverage
- **Format Code**: Format code
- **Sort Imports**: Sort imports
- **Lint Code**: Lint code
- **Type Check**: Type checking
- **Build Package**: Build package
- **Clean Build**: Clean build files
- **Format and Lint**: Run full code quality checks

## Project Dependencies

### Runtime Dependencies

- `pyyaml`: YAML configuration file parsing

### Development Dependencies

- `pytest`: Testing framework
- `pytest-cov`: Test coverage
- `black`: Code formatter
- `isort`: Import sorting
- `flake8`: Linting
- `mypy`: Static type checking

## Release Process

1. Update the version number (in `pyproject.toml`)
2. Run all tests: `uv run pytest`
3. Run code quality checks: `uv run black src tests && uv run isort src tests && uv run flake8 src tests`
4. Build the package: `uv build`
5. Publish to PyPI: `uv publish`

## Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to your branch: `git push origin feature/new-feature`
5. Create a Pull Request

Make sure all tests pass and the code style meets project standards.
