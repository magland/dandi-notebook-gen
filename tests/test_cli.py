"""
Tests for the CLI module
"""

import os
import tempfile
import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from dandi_notebook_gen.cli import cli, main, notebook_gen_cli, notebook_gen_main

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

# Sample data for testing the tools commands
SAMPLE_DANDISET_INFO = {
    "name": "Test Dandiset",
    "description": "A test dandiset for unit testing",
    "id": "000001",
    "version": "draft"
}

SAMPLE_ASSETS = {
    "count": 2,
    "results": [
        {"asset_id": "asset1", "path": "file1.nwb", "size": 1000},
        {"asset_id": "asset2", "path": "file2.nwb", "size": 2000}
    ]
}

SAMPLE_NWB_INFO = {
    "metadata": {
        "session_description": "Test session",
        "identifier": "TEST-NWB-001"
    },
    "neurodata_objects": ["acquisition", "processing"]
}

@patch('dandi_notebook_gen.generator.run_completion')
def test_notebook_gen_command(mock_run_completion):
    """Test the dandi-notebook-gen command functionality"""
    # Mock the run_completion function
    mock_run_completion.return_value = (SAMPLE_AI_RESPONSE, [], 100, 200)

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to the temporary directory
        os.chdir(tmpdir)

        # Run the CLI command
        result = runner.invoke(notebook_gen_cli, ["000001"])

        # Check that the command executed successfully
        assert result.exit_code == 0

        # Check that the output mentions the Dandiset ID
        assert "Dandiset 000001" in result.output

        # Check that the file was created
        assert os.path.exists("dandiset_000001_exploration.py")

@patch('dandi_notebook_gen.generator.run_completion')
def test_notebook_gen_with_output(mock_run_completion):
    """Test the dandi-notebook-gen command with a custom output path"""
    # Mock the run_completion function
    mock_run_completion.return_value = (SAMPLE_AI_RESPONSE, [], 100, 200)

    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a custom output path
        output_path = os.path.join(tmpdir, "custom_notebook.py")

        # Run the CLI command with the output option
        result = runner.invoke(notebook_gen_cli, [
            "000001",
            "--output", output_path
        ])

        # Check that the command executed successfully
        assert result.exit_code == 0

        # Check that the output mentions the custom path
        assert output_path in result.output

        # Check that the file was created at the custom path
        assert os.path.exists(output_path)

@patch('dandi_notebook_gen.tools.dandiset_info')
def test_dandiset_info_command(mock_dandiset_info):
    """Test the dandiset-info subcommand"""
    # Mock the dandiset_info function
    mock_dandiset_info.return_value = SAMPLE_DANDISET_INFO

    runner = CliRunner()
    result = runner.invoke(cli, ["dandiset-info", "000001"])

    # Check that the command executed successfully
    assert result.exit_code == 0

    # Check that the output contains the expected data
    output_data = json.loads(result.output)
    assert output_data["name"] == "Test Dandiset"
    assert output_data["id"] == "000001"

@patch('dandi_notebook_gen.tools.dandiset_assets')
def test_dandiset_assets_command(mock_dandiset_assets):
    """Test the dandiset-assets subcommand"""
    # Mock the dandiset_assets function
    mock_dandiset_assets.return_value = SAMPLE_ASSETS

    runner = CliRunner()
    result = runner.invoke(cli, ["dandiset-assets", "000001", "--page", "1", "--page-size", "10"])

    # Check that the command executed successfully
    assert result.exit_code == 0

    # Check that the output contains the expected data
    output_data = json.loads(result.output)
    assert output_data["count"] == 2
    assert len(output_data["results"]) == 2
    assert output_data["results"][0]["asset_id"] == "asset1"

@patch('dandi_notebook_gen.tools.nwb_file_info')
def test_nwb_file_info_command(mock_nwb_file_info):
    """Test the nwb-file-info subcommand"""
    # Mock the nwb_file_info function
    mock_nwb_file_info.return_value = SAMPLE_NWB_INFO

    runner = CliRunner()
    result = runner.invoke(cli, [
        "nwb-file-info",
        "000001",
        "https://api.dandiarchive.org/api/assets/asset1/download/"
    ])

    # Check that the command executed successfully
    assert result.exit_code == 0

    # Check that the output contains the expected data
    output_data = json.loads(result.output)
    assert "metadata" in output_data
    assert output_data["metadata"]["identifier"] == "TEST-NWB-001"
    assert "neurodata_objects" in output_data

def test_main_function():
    """Test that the main function calls the cli function"""
    runner = CliRunner()
    with patch('dandi_notebook_gen.cli.cli') as mock_cli:
        # Set up the mock
        mock_cli.return_value = None

        # Call the main function
        main()

        # Verify that cli was called
        mock_cli.assert_called_once()

def test_notebook_gen_main_function():
    """Test that the notebook_gen_main function calls the notebook_gen_cli function"""
    runner = CliRunner()
    with patch('dandi_notebook_gen.cli.notebook_gen_cli') as mock_notebook_gen_cli:
        # Set up the mock
        mock_notebook_gen_cli.return_value = None

        # Call the notebook_gen_main function
        notebook_gen_main()

        # Verify that notebook_gen_cli was called
        mock_notebook_gen_cli.assert_called_once()
