"""
Tests for the CLI module
"""

import os
import tempfile
from click.testing import CliRunner
from dandi_notebook_gen.cli import main

def test_cli_basic():
    """Test the basic CLI functionality"""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to the temporary directory
        os.chdir(tmpdir)

        # Run the CLI command
        result = runner.invoke(main, ["000001"])

        # Check that the command executed successfully
        assert result.exit_code == 0

        # Check that the output mentions the Dandiset ID
        assert "Dandiset 000001" in result.output

        # Check that the file was created
        assert os.path.exists("dandiset_000001_exploration.py")

def test_cli_with_output():
    """Test the CLI with a custom output path"""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a custom output path
        output_path = os.path.join(tmpdir, "custom_notebook.py")

        # Run the CLI command with the output option
        result = runner.invoke(main, ["000001", "--output", output_path])

        # Check that the command executed successfully
        assert result.exit_code == 0

        # Check that the output mentions the custom path
        assert output_path in result.output

        # Check that the file was created at the custom path
        assert os.path.exists(output_path)
