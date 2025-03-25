# dandi-notebook-gen

Python package for generating notebooks for Dandisets

## Installation

You can install the package directly from the repository:

```bash
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Generate a notebook for a specific Dandiset
dandi-notebook-gen 000001

# Specify an output path
dandi-notebook-gen 000001 --output my_notebook.py
```

### Python API

```python
from dandi_notebook_gen.generator import generate_notebook

# Generate a notebook for a specific Dandiset
output_path = generate_notebook("000001")
print(f"Generated notebook script at: {output_path}")
```

### Converting to Jupyter Notebook

The package generates Python scripts in jupytext format. To convert to a Jupyter notebook:

```bash
# Install jupytext if not already installed
pip install jupytext

# Convert the Python script to a notebook
jupytext --to notebook dandiset_000001_exploration.py
```

## Development

This package uses [hatchling](https://hatch.pypa.io/) for packaging.

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/magland/dandi-notebook-gen.git
cd dandi-notebook-gen

# Install in development mode with development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Testing

This package uses pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=dandi_notebook_gen
```
