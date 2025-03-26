"""
Python script generator for Dandisets using jupytext format and AI completion
"""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from minicline import perform_task

def read_instructions() -> str:
    """
    Read the instructions from the markdown file.

    Returns
    -------
    str
        The instructions content.
    """
    prompt_path = Path(__file__).parent / "instructions.md"
    with open(prompt_path, 'r') as f:
        return f.read()

def generate_notebook(dandiset_id: str, output_path=None, model="anthropic/claude-3.5-sonnet"):
    """
    Generate a Python script in jupytext format for exploring a Dandiset.

    Parameters
    ----------
    dandiset_id : str
        The ID of the Dandiset to generate a notebook for.
    output_path : str, optional
        Path where the script should be saved. If None, a default path will be used.
    model : str, optional
        The AI model to use for generating the notebook content.

    Returns
    -------
    str
        Path to the generated script.
    """
    # Determine the output path
    if output_path is None:
        output_path = f"dandiset_{dandiset_id}_exploration.ipynb"

    instructions = read_instructions()
    # replace {{ DANDISET_ID }} with the actual dandiset_id
    instructions = instructions.replace("{{ DANDISET_ID }}", dandiset_id)

    # Create a temporary directory
    with TemporaryDirectory() as temp_dir:
        # perform the task which should ultimately create a notebook.py
        perform_task(
            instructions=instructions,
            model=model,
            cwd=temp_dir,
        )
        # check that the notebook.ipynb was created
        notebook_path = os.path.join(temp_dir, "notebook.ipynb")
        if not os.path.exists(notebook_path):
            raise FileNotFoundError("notebook.ipynb was not created")
        # move the notebook.ipynb to the output path
        os.rename(notebook_path, output_path)

    return output_path
