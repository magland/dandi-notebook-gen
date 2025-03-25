"""
Python script generator for Dandisets using jupytext format
"""

import os

def generate_notebook(dandiset_id, output_path=None):
    """
    Generate a Python script in jupytext format for exploring a Dandiset.

    Parameters
    ----------
    dandiset_id : str
        The ID of the Dandiset to generate a notebook for.
    output_path : str, optional
        Path where the script should be saved. If None, a default path will be used.

    Returns
    -------
    str
        Path to the generated script.
    """
    # Determine the output path
    if output_path is None:
        output_path = f"dandiset_{dandiset_id}_exploration.py"

    # Create the content of the Python script with jupytext markers
    content = f'''# ---
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
# # Exploring Dandiset {dandiset_id}
#
# This is a placeholder notebook for exploring Dandiset {dandiset_id}.

# %%
# Placeholder for code
# The actual notebook content will be filled in later

'''

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    # Write the script to a file
    with open(output_path, 'w') as f:
        f.write(content)

    return output_path
