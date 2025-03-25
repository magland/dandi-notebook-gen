"""
Tests for the generator module
"""

import os
import tempfile
from dandi_notebook_gen.generator import generate_notebook

def test_generate_notebook():
    """Test that a notebook can be generated"""
    # Use a temporary directory for the output
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test_notebook.py")

        # Generate a notebook for a test Dandiset ID
        result_path = generate_notebook("000001", output_path)

        # Check that the file was created
        assert os.path.exists(result_path)

        # Check that the file contains the expected content
        with open(result_path, 'r') as f:
            content = f.read()
            assert "# Exploring Dandiset 000001" in content
            assert "This is a placeholder notebook" in content
            assert "jupytext" in content
