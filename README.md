# dandi-notebook-gen

Python package for generating AI-powered notebooks for exploring Dandisets and working with DANDI datasets

## Installation

You can install the package directly from the repository:

```bash
pip install -e .
```

## Configuration

This package uses the minicline library to interact with AI models. Configuration may be required depending on the AI model being used. See the minicline documentation for more details.

## Usage

### Command Line Interface

The package provides two command-line tools:

#### Generate a Notebook

Use the `dandi-notebook-gen` command:

```bash
# Generate a notebook for a specific Dandiset
dandi-notebook-gen 000001

# Specify an output path
dandi-notebook-gen 000001 --output my_notebook.py
```

#### Get Dandiset Information

```bash
# Get information about a Dandiset
dandi-notebook-gen-tools dandiset-info 000001

# Specify a version (default is "draft")
dandi-notebook-gen-tools dandiset-info 000001 --version 0.220127.2115

# Save the output to a file
dandi-notebook-gen-tools dandiset-info 000001 --output info.json
```

#### List Dandiset Assets

```bash
# List assets in a Dandiset
dandi-notebook-gen-tools dandiset-assets 000001

# Filter assets by file pattern
dandi-notebook-gen-tools dandiset-assets 000001 --glob "*.nwb"

# Paginate results
dandi-notebook-gen-tools dandiset-assets 000001 --page 2 --page-size 50

# Save the output to a file
dandi-notebook-gen-tools dandiset-assets 000001 --output assets.json
```

#### Get NWB File Information

```bash
# Get information about an NWB file
dandi-notebook-gen-tools nwb-file-info 000001 https://api.dandiarchive.org/api/assets/ASSET_ID/download/

# Save the output to a file
dandi-notebook-gen-tools nwb-file-info 000001 https://api.dandiarchive.org/api/assets/ASSET_ID/download/ --output nwb_info.json
```

### Python API

#### Generate a Notebook

```python
from dandi_notebook_gen.generator import generate_notebook

# Generate a notebook for a specific Dandiset
output_path = generate_notebook("000001")
print(f"Generated notebook script at: {output_path}")

# Specify a different AI model
output_path = generate_notebook("000001", model="anthropic/claude-3-sonnet:beta")
```

#### Use DANDI Tools

```python
from dandi_notebook_gen.tools import dandiset_info, dandiset_assets, nwb_file_info

# Get information about a Dandiset
info = dandiset_info("000001")

# List assets in a Dandiset
assets = dandiset_assets("000001", glob="*.nwb", page=1, page_size=10)

# Get information about an NWB file
nwb_info = nwb_file_info("000001", "https://api.dandiarchive.org/api/assets/ASSET_ID/download/")
```

### Converting to Jupyter Notebook

The package generates Python scripts in jupytext format. To convert to a Jupyter notebook:

```bash
# Install jupytext if not already installed
pip install jupytext

# Convert the Python script to a notebook
jupytext --to notebook dandiset_000001_exploration.py
```

## Logging

The package uses the minicline library to handle AI interactions. Logging functionality may be available through this library.

## How It Works

The package uses AI to generate a comprehensive notebook for exploring a Dandiset:

1. It uses the minicline library to perform tasks with AI models
2. The AI uses tools to gather information about the Dandiset, including metadata and file listings
3. The AI generates a notebook with explanatory text and code for exploring the dataset
4. The notebook is formatted as a jupytext Python file that can be converted to a Jupyter notebook

## DANDI Tools

The package includes several tools for working with DANDI datasets:

### dandiset_info

Get detailed information about a DANDI dataset, including:
- Name and description
- Access and license information
- Citation details
- Keywords and protocol
- Contributor names
- Date created
- Size and number of files
- Number of subjects
- Variables measured
- Measurement techniques

### dandiset_assets

Get a list of assets/files in a DANDI dataset, including:
- Total count of assets
- Asset IDs
- File paths
- File sizes

### nwb_file_info

Get information about an NWB file, including:
- Metadata
- Information about neurodata objects
- Instructions for loading the data using pynwb and lindi

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
