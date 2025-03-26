"""
Tests for the generator module
"""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from dandi_notebook_gen.generator import generate_notebook, clean_content, run_generated_script

# Sample AI response for testing (already in jupytext format)
SAMPLE_AI_RESPONSE = """<python_code>
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Exploring Dandiset 000001
#
# This is a test notebook for exploring Dandiset 000001.

# %%
import numpy as np
import matplotlib.pyplot as plt
from dandi.dandiapi import DandiAPIClient

# Connect to the DANDI API
client = DandiAPIClient()

# %% [markdown]
# ## Dataset Information
#
# Let's explore the dataset metadata.

# %%
# Get dataset info
dandiset = client.get_dandiset('000001')
print(f"Dataset name: {dandiset.get('name')}")
</python_code>
"""

def test_clean_content():
    """Test the cleaning of AI response content"""
    # Test with python_code tags
    content_with_python_tags = "<python_code>Some python content</python_code>"
    result = clean_content(content_with_python_tags)
    assert result == "Some python content"

    # Test with result tags (backward compatibility)
    content_with_result_tags = "<result>Some content</result>"
    result = clean_content(content_with_result_tags)
    assert result == "Some content"

    # Test without any tags
    content_without_tags = "Some content"
    result = clean_content(content_without_tags)
    assert result == "Some content"

    # Test with both python_code and result tags
    content_with_both_tags = "<python_code><result>Nested content</result></python_code>"
    result = clean_content(content_with_both_tags)
    assert result == "<result>Nested content</result>"

@patch('dandi_notebook_gen.generator.run_completion')
@patch('dandi_notebook_gen.generator.run_generated_script')
def test_generate_notebook(mock_run_generated_script, mock_run_completion):
    """Test that a notebook can be generated"""
    # Mock the run_completion function
    mock_run_completion.return_value = (SAMPLE_AI_RESPONSE, [], 100, 200)

    # Mock the run_generated_script function
    mock_run_generated_script.return_value = (True, "Script output", None)

    # Create a side effect that creates the log directory and a log file
    def run_completion_side_effect(*args, **kwargs):
        # Create the log directory
        log_dir = kwargs.get('log_dir', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        # Create a dummy log file
        log_file = kwargs.get('log_file')
        if log_file is None:
            log_file = 'test_log.json'
        log_path = os.path.join(log_dir, log_file)
        with open(log_path, 'w') as f:
            f.write('[]')
        return (SAMPLE_AI_RESPONSE, [], 100, 200)

    mock_run_completion.side_effect = run_completion_side_effect

    # Use a temporary directory for the output
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test_notebook.py")
        log_dir = os.path.join(tmpdir, "logs")

        # Generate a notebook for a test Dandiset ID
        result_path = generate_notebook("000001", output_path, log_dir=log_dir)

        # Check that the file was created
        assert os.path.exists(result_path)

        # Check that the file contains the expected content
        with open(result_path, 'r') as f:
            content = f.read()
            assert "# jupyter:" in content
            assert "jupytext:" in content
            assert "# %% [markdown]" in content

        # Check that the logs directory was created
        assert os.path.exists(log_dir)

        # Check that a log file was created in the logs directory
        log_files = os.listdir(log_dir)
        assert len(log_files) > 0
        assert any(file.endswith('.json') for file in log_files)

@patch('dandi_notebook_gen.generator.run_completion')
@patch('dandi_notebook_gen.generator.run_generated_script')
def test_generate_notebook_with_custom_log_file(mock_run_generated_script, mock_run_completion):
    """Test that a notebook can be generated with a custom log file"""
    # Mock the run_completion function
    mock_run_completion.return_value = (SAMPLE_AI_RESPONSE, [], 100, 200)

    # Mock the run_generated_script function
    mock_run_generated_script.return_value = (True, "Script output", None)

    # Create a side effect that creates the log directory and a log file
    def run_completion_side_effect(*args, **kwargs):
        # Create the log directory
        log_dir = kwargs.get('log_dir', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        # Create a dummy log file
        log_file = kwargs.get('log_file')
        if log_file is None:
            log_file = 'test_log.json'
        log_path = os.path.join(log_dir, log_file)
        with open(log_path, 'w') as f:
            f.write('[]')
        return (SAMPLE_AI_RESPONSE, [], 100, 200)

    mock_run_completion.side_effect = run_completion_side_effect

    # Use a temporary directory for the output
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test_notebook.py")
        log_dir = os.path.join(tmpdir, "logs")
        log_file = "custom_log.json"

        # Generate a notebook for a test Dandiset ID with a custom log file
        result_path = generate_notebook(
            "000001",
            output_path,
            log_dir=log_dir,
            log_file=log_file
        )

        # Check that the file was created
        assert os.path.exists(result_path)

        # Check that the custom log file was created
        custom_log_path = os.path.join(log_dir, log_file)
        assert os.path.exists(custom_log_path)


@patch('dandi_notebook_gen.generator.preprocess_and_run_script')
def test_run_generated_script_success(mock_preprocess_and_run):
    """Test that a script can be run successfully"""
    # Mock the preprocess_and_run_script function
    mock_preprocess_and_run.return_value = (True, "Script output", None)

    # Run a test script
    success, output, error = run_generated_script("test_script.py")

    # Check that the function returns the expected values
    assert success is True
    assert output == "Script output"
    assert error is None

    # Check that preprocess_and_run_script was called with the correct arguments
    mock_preprocess_and_run.assert_called_once_with("test_script.py", capture_output=True)


@patch('dandi_notebook_gen.generator.preprocess_and_run_script')
def test_run_generated_script_failure(mock_preprocess_and_run):
    """Test that a script failure is handled correctly"""
    # Mock the preprocess_and_run_script function to simulate a failure
    mock_preprocess_and_run.return_value = (False, None, "Error message")

    # Run a test script
    success, output, error = run_generated_script("test_script.py")

    # Check that the function returns the expected values
    assert success is False
    assert output is None
    assert error == "Error message"

    # Check that preprocess_and_run_script was called with the correct arguments
    mock_preprocess_and_run.assert_called_once_with("test_script.py", capture_output=True)
