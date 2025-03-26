#!/usr/bin/env python
"""
Example script demonstrating how to use dandi-notebook-gen
"""

from dandi_notebook_gen.generator import generate_notebook

if __name__ == "__main__":
    # Example: Generate a notebook for Dandiset 000004
    dandiset_id = "000004"
    output_path = generate_notebook(dandiset_id)
    print(f"Generated notebook script at: {output_path}")

    # The generated Python script is already in jupytext format and can be opened directly in Jupyter
    # Or you can convert it to a .ipynb file using jupytext:
    # jupytext --to notebook dandiset_000004_exploration.py
