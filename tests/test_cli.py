"""
Tests for the CLI module
"""

import os
import tempfile
import pytest
from unittest.mock import patch
from click.testing import CliRunner
from dandi_notebook_gen.cli import main

# Sample AI response for testing (same as in test_generator.py)
SAMPLE_AI_RESPONSE = """
# Exploring Dandiset 000001

This is a test notebook for exploring Dandiset 000001.

```python
import numpy as np
import matplotlib.pyplot as plt
from dandi.dandiapi import DandiAPIClient

# Connect to the DANDI API
client = DandiAPIClient()
```

## Dataset Information

Let's explore the dataset metadata.

```python
# Get dataset info
dandiset = client.get_dandiset('000001')
print(f"Dataset name: {dandiset.get('name')}")
```
"""

@patch('dandi_notebook_gen.generator.run_completion')
def test_cli_basic(mock_run_completion):
    """Test the basic CLI functionality"""
    # Mock the run_completion function
    mock_run_completion.return_value = (SAMPLE_AI_RESPONSE, [], 100, 200)

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to the temporary directory
        os.chdir(tmpdir)

        # Create a logs directory
        logs_dir = os.path.join(tmpdir, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Run the CLI command
        result = runner.invoke(main, ["000001", "--log-dir", logs_dir])

        # Check that the command executed successfully
        assert result.exit_code == 0

        # Check that the output mentions the Dandiset ID
        assert "Dandiset 000001" in result.output

        # Check that the file was created
        assert os.path.exists("dandiset_000001_exploration.py")

@patch('dandi_notebook_gen.generator.run_completion')
def test_cli_with_output(mock_run_completion):
    """Test the CLI with a custom output path"""
    # Mock the run_completion function
    mock_run_completion.return_value = (SAMPLE_AI_RESPONSE, [], 100, 200)

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a custom output path
        output_path = os.path.join(tmpdir, "custom_notebook.py")

        # Create a logs directory
        logs_dir = os.path.join(tmpdir, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Create a custom log file name
        log_file = "test_log.json"

        # Run the CLI command with the output option
        result = runner.invoke(main, [
            "000001",
            "--output", output_path,
            "--log-dir", logs_dir,
            "--log-file", log_file
        ])

        # Check that the command executed successfully
        assert result.exit_code == 0

        # Check that the output mentions the custom path
        assert output_path in result.output

        # Check that the file was created at the custom path
        assert os.path.exists(output_path)
