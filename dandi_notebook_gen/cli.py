"""
Command-line interface for dandi-notebook-gen
"""

import click
from .generator import generate_notebook

@click.command()
@click.argument("dandiset_id", type=str)
@click.option("--output", "-o", default=None, help="Output file path for the notebook")
def main(dandiset_id, output):
    """
    Generate a Jupyter notebook for exploring a Dandiset.

    DANDISET_ID: The ID of the Dandiset to generate a notebook for.
    """
    click.echo(f"Generating notebook for Dandiset {dandiset_id}")

    try:
        notebook_path = generate_notebook(dandiset_id, output)
        click.echo(f"Notebook generated successfully: {notebook_path}")
    except Exception as e:
        click.echo(f"Error generating notebook: {str(e)}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    main()
