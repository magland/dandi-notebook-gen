"""
Python script generator for Dandisets using jupytext format and AI completion
"""

from typing import Union
import os
import json
import shutil
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from minicline import perform_task

def read_instructions(experimental_mode: bool = False, scientific_mode: bool = False) -> str:
    """
    Read the instructions from the markdown file.

    Parameters
    ----------
    experimental_mode : bool, optional
        Whether to use experimental mode instructions.
    scientific_mode : bool, optional
        Whether to use scientific findings mode instructions.

    Returns
    -------
    str
        The instructions content.
    """
    prompt_path = Path(__file__).parent / "instructions_v2.txt"
    if experimental_mode:
        prompt_path = Path(__file__).parent / "instructions_experimental.md"
    elif scientific_mode:
        prompt_path = Path(__file__).parent / "instructions_scientific_findings.md"
    with open(prompt_path, 'r') as f:
        return f.read()

def generate_notebook(dandiset_id: str = None, output_path=None, *, phenomenon: str = None, model="google/gemini-2.0-flash-001", vision_model: Union[str, None]=None, auto: bool=False, approve_all_commands: bool=False, working_dir: Union[str, None]=None, experimental_mode=False, scientific_mode=False) -> str:
    """
    Generate a Python script in jupytext format for exploring a Dandiset or demonstrating a scientific phenomenon.

    Parameters
    ----------
    dandiset_id : str, optional
        The ID of the Dandiset to generate a notebook for. Required for standard and experimental modes.
        In scientific_mode, this can be None and will be determined during the notebook generation.
    phenomenon : str, optional
        The scientific phenomenon to demonstrate. Required for scientific_mode.
    output_path : str, optional
        Path where the script should be saved. If None, a default path will be used.
    model : str, optional
        The AI model to use for generating the notebook content.
    vision_model : str, optional
        The AI model to use for analyzing images. If None, the model parameter will be used.
    auto : bool, optional
        Whether to run minicline in auto mode.
    approve_all_commands : bool, optional
        Whether to run minicline in approve_all_commands mode.
    working_dir : str, optional
        The working directory to use for the task. If not provided, a temporary directory will be used.

    Returns
    -------
    str
        Path to the generated script.
    """
    # Determine the output path
    if output_path is None:
        if scientific_mode:
            output_path = f"{phenomenon.lower().replace(' ', '_')}_demonstration.ipynb"
        else:
            output_path = f"dandiset_{dandiset_id}_exploration.ipynb"
    if not output_path.endswith(".ipynb"):
        raise ValueError("Output path must end with '.ipynb'")

    if approve_all_commands and not auto:
        raise ValueError("approve_all_commands can only be used with auto mode")

    if not vision_model:
        vision_model = model

    if scientific_mode:
        if phenomenon is None:
            raise ValueError("phenomenon parameter is required in scientific_mode")
        instructions = read_instructions(scientific_mode=scientific_mode)
        # replace {{ PHENOMENON }} with the actual phenomenon
        instructions = instructions.replace("{{ PHENOMENON }}", phenomenon)
    else:
        if dandiset_id is None:
            raise ValueError("dandiset_id parameter is required in standard and experimental modes")
        instructions = read_instructions(experimental_mode=experimental_mode)
        # replace {{ DANDISET_ID }} with the actual dandiset_id
        instructions = instructions.replace("{{ DANDISET_ID }}", dandiset_id)

    start_time = time.time()
    def helper(working_dir: str):
        print(f'Using working directory: {working_dir}')
        # perform the task which should ultimately create a notebook.py
        perform_task_result = perform_task(
            instructions=instructions,
            model=model,
            vision_model=vision_model,
            cwd=working_dir,
            auto=auto,
            approve_all_commands=approve_all_commands,
            log_file=f'{working_dir}/minicline.log'
        )
        total_prompt_tokens = perform_task_result.total_prompt_tokens
        total_completion_tokens = perform_task_result.total_completion_tokens
        total_vision_prompt_tokens = perform_task_result.total_vision_prompt_tokens
        total_vision_completion_tokens = perform_task_result.total_vision_completion_tokens
        with open(f'{working_dir}/metadata.json', 'w') as f:
            elapsed_time = time.time() - start_time
            json.dump({
                'model': model,
                'vision_model': vision_model,
                'total_prompt_tokens': total_prompt_tokens,
                'total_completion_tokens': total_completion_tokens,
                'total_vision_prompt_tokens': total_vision_prompt_tokens,
                'total_vision_completion_tokens': total_vision_completion_tokens,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'elapsed_time_seconds': elapsed_time
            }, f, indent=2)
        # check that the notebook.ipynb was created
        notebook_path = os.path.join(working_dir, "notebook.ipynb")
        if not os.path.exists(notebook_path):
            raise FileNotFoundError("notebook.ipynb was not created")
        # copy the notebook.ipynb to the output path
        shutil.copy(notebook_path, output_path)

    # Create a temporary directory
    if working_dir is not None:
        os.makedirs(working_dir, exist_ok=True)
        helper(working_dir=working_dir)
    else:
        with TemporaryDirectory() as temp_dir:
            helper(working_dir=temp_dir)


    return output_path
