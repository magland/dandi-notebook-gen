# dandi-notebook-gen

Python package for generating AI-powered notebooks for exploring Dandisets

## Installation

You can install the package directly from the repository:

```bash
pip install -e .
```

## Configuration

This package requires an OpenRouter API key to generate notebooks. You can set it as an environment variable:

```bash
export OPENROUTER_API_KEY=your_api_key_here
```

Alternatively, you can create a `.env` file in the project root with the following content:

```
OPENROUTER_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface

```bash
# Generate a notebook for a specific Dandiset
dandi-notebook-gen 000001

# Specify an output path
dandi-notebook-gen 000001 --output my_notebook.py

# Specify a custom log directory
dandi-notebook-gen 000001 --log-dir custom_logs

# Specify a custom log file name
dandi-notebook-gen 000001 --log-file my_log.json
```

### Python API

```python
from dandi_notebook_gen.generator import generate_notebook

# Generate a notebook for a specific Dandiset
output_path = generate_notebook("000001")
print(f"Generated notebook script at: {output_path}")

# Specify a different AI model
output_path = generate_notebook("000001", model="anthropic/claude-3-sonnet:beta")

# Specify custom logging options
output_path = generate_notebook(
    "000001",
    log_dir="custom_logs",
    log_file="my_log.json"
)
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

The package automatically logs all AI interactions to JSON files. These logs include:

- Input messages sent to the AI
- Output content received from the AI
- Complete conversation history including tool calls
- Token usage statistics
- Metadata about the Dandiset and generation process
- Timestamps

### Log File Location

By default, logs are stored in a `logs` directory in the current working directory. Each log file is named with a timestamp (e.g., `ai_log_20250325_144530.json`).

You can customize the log location using command-line options:

```bash
# Specify a custom log directory
dandi-notebook-gen 000001 --log-dir custom_logs

# Specify a custom log file name
dandi-notebook-gen 000001 --log-file my_log.json
```

Or when using the Python API:

```python
generate_notebook("000001", log_dir="custom_logs", log_file="my_log.json")
```

### Log File Format

The log files are in JSON format and contain an array of log entries. Each entry includes:

```json
{
  "timestamp": "2025-03-25T14:45:30.123456",
  "model": "anthropic/claude-3-opus:beta",
  "input_messages": [...],
  "output_content": "...",
  "conversation_messages": [...],
  "token_usage": {
    "prompt_tokens": 1234,
    "completion_tokens": 5678,
    "total_tokens": 6912
  },
  "metadata": {
    "dandiset_id": "000001",
    "output_path": "dandiset_000001_exploration.py",
    "timestamp": "2025-03-25T14:45:30.123456"
  }
}
```

You can use standard JSON tools to analyze these logs or write custom scripts to extract information about token usage, conversation patterns, and more.

## How It Works

The package uses AI to generate a comprehensive notebook for exploring a Dandiset:

1. It sends a request to the OpenRouter API with a system prompt that guides the AI to create a notebook
2. The AI uses tools to gather information about the Dandiset, including metadata and file listings
3. The AI generates a notebook with explanatory text and code for exploring the dataset
4. The notebook is formatted as a jupytext Python file that can be converted to a Jupyter notebook

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
