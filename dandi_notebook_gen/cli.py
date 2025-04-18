"""
Command-line interfaces for dandi-notebook-gen and dandi-notebook-gen-tools
"""

import json
import click
from .generator import generate_notebook
from .tools import dandiset_assets, nwb_file_info, dandiset_info

@click.command(name="dandi-notebook-gen")
@click.argument("dandiset_id", type=str)
@click.option("--output", "-o", default=None, help="Output file path for the notebook")
@click.option("--model", "-m", default="anthropic/claude-3.7-sonnet", help="OpenRouter model name")
@click.option("--vision-model", "-vm", default=None, help="OpenRouter model name for analyzing images. If not provided, the model parameter will be used.")
@click.option("--auto", is_flag=True, help="Run minicline in auto mode")
@click.option("--approve-all-commands", is_flag=True, help="Run minicline in approve_all_commands mode")
@click.option("--working-dir", default=None, help="Working directory to use for the task. If not provided, a temporary directory will be used.")
def notebook_gen_cli(dandiset_id, output, model, vision_model, auto, approve_all_commands, working_dir):
    """
    Generate a Jupyter notebook for exploring a Dandiset.

    DANDISET_ID: The ID of the Dandiset to generate a notebook for.
    """
    click.echo(f"Generating notebook for Dandiset {dandiset_id}")

    try:
        notebook_path = generate_notebook(dandiset_id, output_path=output, model=model, vision_model=vision_model, auto=auto, approve_all_commands=approve_all_commands, working_dir=working_dir if working_dir else None)
        click.echo(f"Notebook generated successfully: {notebook_path}")
    except Exception as e:
        click.echo(f"Error generating notebook: {str(e)}", err=True)
        raise click.Abort()

@click.group(name="dandi-notebook-gen-tools")
def cli():
    """Tools for working with DANDI datasets."""
    pass

@cli.command(name="dandiset-assets")
@click.argument("dandiset_id", type=str)
@click.option("--version", default="draft", help="Version of the dataset to retrieve")
@click.option("--page", type=int, default=1, help="Page number")
@click.option("--page-size", type=int, default=20, help="Number of results per page")
@click.option("--glob", default=None, help="Optional glob pattern to filter files (e.g., '*.nwb')")
@click.option("--output", "-o", default=None, help="Output file path for the results (default: print to stdout)")
def assets(dandiset_id, version, page, page_size, glob, output):
    """
    Get a list of assets/files in a dandiset version.

    DANDISET_ID: The ID of the Dandiset to retrieve assets for.
    """
    try:
        result = dandiset_assets(
            dandiset_id=dandiset_id,
            version=version,
            page=page,
            page_size=page_size,
            glob=glob
        )

        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error retrieving dandiset assets: {str(e)}", err=True)
        raise click.Abort()

@cli.command(name="nwb-file-info")
@click.argument("dandiset_id", type=str)
@click.argument("nwb_file_url", type=str)
@click.option("--output", "-o", default=None, help="Output file path for the results (default: print to stdout)")
def nwb_info(dandiset_id, nwb_file_url, output):
    """
    Get information about an NWB file.

    DANDISET_ID: The ID of the Dandiset containing the NWB file.
    NWB_FILE_URL: URL of the NWB file in the DANDI archive.
    """
    try:
        result = nwb_file_info(
            dandiset_id=dandiset_id,
            nwb_file_url=nwb_file_url
        )

        if output:
            with open(output, 'w') as f:
                if type(result) == str:
                    f.write(result)
                else:
                    json.dump(result, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            if type(result) == str:
                click.echo(result)
            else:
                click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error retrieving NWB file info: {str(e)}", err=True)
        raise click.Abort()

@cli.command(name="dandiset-info")
@click.argument("dandiset_id", type=str)
@click.option("--version", default="draft", help="Version of the dataset to retrieve")
@click.option("--output", "-o", default=None, help="Output file path for the results (default: print to stdout)")
def dataset_info(dandiset_id, version, output):
    """
    Get information about a specific version of a DANDI dataset.

    DANDISET_ID: The ID of the Dandiset to retrieve information for.
    """
    try:
        result = dandiset_info(
            dandiset_id=dandiset_id,
            version=version
        )

        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error retrieving dandiset info: {str(e)}", err=True)
        raise click.Abort()

def main():
    """Entry point for the dandi-notebook-gen-tools CLI."""
    cli()

def notebook_gen_main():
    """Entry point for the dandi-notebook-gen CLI."""
    notebook_gen_cli()

if __name__ == "__main__":
    main()
