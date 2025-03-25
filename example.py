#!/usr/bin/env python
"""
Example script demonstrating how to use dandi-notebook-gen
"""

from dandi_notebook_gen.generator import generate_notebook

if __name__ == "__main__":
    # Example: Generate a notebook for Dandiset 000001
    dandiset_id = "000001"
    output_path = generate_notebook(dandiset_id)
    print(f"Generated notebook script at: {output_path}")

    # To convert the generated Python script to a Jupyter notebook, you can use jupytext:
    # jupytext --to notebook dandiset_000001_exploration.py
