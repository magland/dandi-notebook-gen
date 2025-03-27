# dandi-notebook-gen

Python package for generating AI-powered notebooks for exploring Dandisets and working with DANDI datasets

## Installation

You can install the package directly from the repository:

```bash
pip install .
```

## Configuration

This package uses the minicline library to interact with AI models. See the [minicline](https://github.com/magland/minicline) documentation for more details.

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

This tool is used internally by the notebook generator, but can also be used directly:

```bash
# Get information about a Dandiset
dandi-notebook-gen-tools dandiset-info 000001

# Specify a version (default is "draft")
dandi-notebook-gen-tools dandiset-info 000001 --version 0.220127.2115

# Save the output to a file
dandi-notebook-gen-tools dandiset-info 000001 --output info.json
```

#### List Dandiset Assets

This tool is used internally by the notebook generator, but can also be used directly:

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

This tool is used internally by the notebook generator, but can also be used directly:

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
output_path = generate_notebook("000001", model="anthropic/claude-3.5-sonnet")
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

## How It Works

The package uses AI to generate a comprehensive notebook for exploring a Dandiset:

1. It uses the minicline library to perform tasks with AI models
2. Uses tools to gather information about the Dandiset, including metadata and file listings\
3. Uses exploratory analysis on the Dandiset, including creating an executing scripts, generating plots, and using AI vision to interpret the plots.
4. Generates a notebook with explanatory text and code for exploring the dataset

## Development

This package uses [hatchling](https://hatch.pypa.io/) for packaging.

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/magland/dandi-notebook-gen.git
cd dandi-notebook-gen

# Install in development mode with development dependencies
pip install -e ".[dev]"
```
