"""
Command-line interface for dandi-notebook-gen
"""

import click
from .generator import generate_notebook

@click.command()
@click.argument("dandiset_id", type=str)
@click.option("--output", "-o", default=None, help="Output file path for the notebook")
@click.option("--log-dir", default="logs", help="Directory where log files will be stored")
@click.option("--log-file", default=None, help="Name of the log file (default: auto-generated timestamp)")
def main(dandiset_id, output, log_dir, log_file):
    """
    Generate a Jupyter notebook for exploring a Dandiset.

    DANDISET_ID: The ID of the Dandiset to generate a notebook for.
    """
    click.echo(f"Generating notebook for Dandiset {dandiset_id}")

    try:
        notebook_path = generate_notebook(dandiset_id, output, log_dir=log_dir, log_file=log_file)
        click.echo(f"Notebook generated successfully: {notebook_path}")
    except Exception as e:
        click.echo(f"Error generating notebook: {str(e)}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    main()
