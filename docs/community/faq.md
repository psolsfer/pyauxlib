# Frequently Asked Questions

## Installation Issues

### Q: I'm getting an error when installing pyauxlib

A: Make sure you have Python 3.10+ installed and try upgrading pip:

```bash
pip install --upgrade pip
pip install pyauxlib
```

## Usage Issues

### Q: How do I get started with pyauxlib?

A: Check out the [Usage](../getting-started/usage.md) and [Installation](../getting-started/installation.md) guides.

## Development Issues

### Q: Tests are failing in my development environment

A: Make sure you've installed all development dependencies:

```bash
uv sync
```

### Q: My code style checks are failing

A: Run the formatters and linters:

```bash
uv run ruff format .
uv run ruff check --fix .
```

## General Questions

### Q: How can I contribute to pyauxlib?

A: See the [Contributing](contributing.md) guide for details.

### Q: Where can I report bugs or request features?

A: Please use the [GitHub Issues](https://github.com/psolsfer/pyauxlib/issues) page.
