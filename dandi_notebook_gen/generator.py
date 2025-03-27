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

def generate_notebook(dandiset_id: str, output_path=None, *, model="google/gemini-2.0-flash-001", auto: bool=False, approve_all_commands: bool=False) -> str:
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
    auto : bool, optional
        Whether to run minicline in auto mode.
    approve_all_commands : bool, optional
        Whether to run minicline in approve_all_commands mode.

    Returns
    -------
    str
        Path to the generated script.
    """
    # Determine the output path
    if output_path is None:
        output_path = f"dandiset_{dandiset_id}_exploration.ipynb"
    if not output_path.endswith(".ipynb"):
        raise ValueError("Output path must end with '.ipynb'")

    if approve_all_commands and not auto:
        raise ValueError("approve_all_commands can only be used with auto mode")

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
            auto=auto,
            approve_all_commands=approve_all_commands
        )
        # check that the notebook.ipynb was created
        notebook_path = os.path.join(temp_dir, "notebook.ipynb")
        if not os.path.exists(notebook_path):
            raise FileNotFoundError("notebook.ipynb was not created")
        # move the notebook.ipynb to the output path
        os.rename(notebook_path, output_path)

    return output_path
