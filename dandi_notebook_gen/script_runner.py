"""
Module for running jupytext notebook scripts with preprocessing capabilities
"""

import re
import sys
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List


def check_for_matplotlib(script_content: str) -> bool:
    """
    Check if the script uses matplotlib for plotting.

    Parameters
    ----------
    script_content : str
        The content of the Python script.

    Returns
    -------
    bool
        True if matplotlib is used for plotting, False otherwise.
    """
    # Check for matplotlib import
    if re.search(r'import\s+matplotlib|from\s+matplotlib', script_content):
        # Check for plotting functions
        if re.search(r'\.plot\(|\.imshow\(|\.scatter\(|\.hist\(|\.bar\(|plt\.show\(|\.figure\(', script_content):
            return True
    return False


def add_matplotlib_backend(script_content: str) -> str:
    """
    Add a line at the top of the script to set the matplotlib backend to 'Agg'
    to prevent plots from showing.

    Parameters
    ----------
    script_content : str
        The content of the Python script.

    Returns
    -------
    str
        The modified script content with the matplotlib backend set.
    """
    # Check if matplotlib is already imported
    if re.search(r'import\s+matplotlib', script_content):
        # Add backend setting after the import
        return re.sub(
            r'(import\s+matplotlib.*?)(\n)',
            r'\1\nimport matplotlib\nmatplotlib.use("Agg")\2',
            script_content,
            count=1
        )
    elif re.search(r'from\s+matplotlib', script_content):
        # Add import and backend setting before the first matplotlib import
        return re.sub(
            r'(from\s+matplotlib.*?)(\n)',
            r'import matplotlib\nmatplotlib.use("Agg")\n\1\2',
            script_content,
            count=1
        )
    else:
        # If no matplotlib import found (unlikely given the check_for_matplotlib check),
        # add it at the top of the file
        return f'import matplotlib\nmatplotlib.use("Agg")\n\n{script_content}'


def run_script(script_path: str, capture_output: bool = True) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Run a Python script and capture its output and errors.

    Parameters
    ----------
    script_path : str
        Path to the Python script to run.
    capture_output : bool, optional
        Whether to capture the output of the script. Default is True.

    Returns
    -------
    Tuple[bool, Optional[str], Optional[str]]
        A tuple containing:
        - success: True if the script ran successfully, False otherwise.
        - output: The standard output of the script if capture_output is True, None otherwise.
        - error: The standard error of the script if it failed and capture_output is True, None otherwise.
    """
    try:
        if capture_output:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                check=False
            )
            return (
                result.returncode == 0,
                result.stdout if result.stdout else None,
                result.stderr if result.stderr and result.returncode != 0 else None
            )
        else:
            # Run without capturing output (displays in real-time)
            result = subprocess.run([sys.executable, script_path], check=False)
            return result.returncode == 0, None, None
    except Exception as e:
        return False, None, str(e)


def preprocess_and_run_script(script_path: str, capture_output: bool = True) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Preprocess a Python script to handle matplotlib plots and then run it.
    If the script uses matplotlib, a new file with '_run' suffix is created with the modified content.

    Parameters
    ----------
    script_path : str
        Path to the Python script to preprocess and run.
    capture_output : bool, optional
        Whether to capture the output of the script. Default is True.

    Returns
    -------
    Tuple[bool, Optional[str], Optional[str]]
        A tuple containing:
        - success: True if the script ran successfully, False otherwise.
        - output: The standard output of the script if capture_output is True, None otherwise.
        - error: The standard error of the script if it failed and capture_output is True, None otherwise.
    """
    script_path = Path(script_path)

    # Read the script content
    with open(script_path, 'r') as f:
        script_content = f.read()

    # Check if the script uses matplotlib for plotting
    if check_for_matplotlib(script_content):
        # Add matplotlib backend setting to prevent plots from showing
        modified_content = add_matplotlib_backend(script_content)

        # Create a new file path with '_run' suffix
        run_script_path = script_path.with_stem(f"{script_path.stem}_run")

        # Write the modified content to the new file
        with open(run_script_path, 'w') as f:
            f.write(modified_content)

        # Run the modified script
        return run_script(str(run_script_path), capture_output)
    else:
        # Run the original script if no matplotlib is used
        return run_script(str(script_path), capture_output)
