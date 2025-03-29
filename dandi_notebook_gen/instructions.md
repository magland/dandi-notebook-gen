# Notebook Generation Instructions

You are going to create a Jupytext notebook called `notebook.py` that will help researchers explore and analyze a Dandiset {{ DANDISET_ID }}. After you create the notebook, convert it to `notebook.ipynb` and execute the Jupyter notebook to make sure it runs without errors. If there are errors, you will need to fix them in the original `notebook.py` file, re-convert and re-run the notebook, repeating until it runs properly.

The notebook should:

1. Provide an introduction to the Dandiset, including its name, description, and key metadata
2. Include code to load and explore the dataset's structure
3. Demonstrate how to access and visualize sample data from NWB files
4. Include explanatory markdown cells that guide the user through the analysis process
5. Provide examples of common analyses that might be relevant to the dataset's content

Here's the plan that you should follow:
1. Get the Dandiset metadata using `dandi-notebook-gen-tools dandiset-info {{ DANDISET_ID }}`.
2. Get the Dandiset assets using `dandi-notebook-gen-tools dandiset-assets {{ DANDISET_ID }}`.
3. Choose an NWB file from the assets and get its information using `dandi-notebook-gen-tools nwb-file-info {{ DANDISET_ID }} <NWB_FILE_URL>`.
4. Do exploratory research on the contents of the Dandiset by creating and executing python scripts in a tmp_scripts subdirectory to generate text output and plots.
  - It's very important that the plots go to .PNG image files in the tmp_scripts subdirectory. Otherwise, if the plot is displayed in a window, the script will hang. So do not do a plt.show().
  - If the script times out (use a timeout of 90 seconds for the scripts), you may be trying to load too much data. Try revising the script and rerun.
  - After executing each script, if you created plots, always review each plot using the read_image tool to be able to gain information about them. Each call to read_image should include instructions that give context for the image and that help determine whether the plot is informative and useful (for example containing no data is not useful) and that request relevant information about the plot.
5. Write the content of the notebook to `notebook.py`, including the introduction, dataset structure exploration, sample data access and visualization, explanatory markdown cells, and examples of common analyses.
6. Run `jupytext --to notebook notebook.py && jupyter execute --inplace notebook.ipynb` to convert the notebook to a Jupyter notebook and execute the resulting `notebook.ipynb` to make sure it runs without errors and produces output cells. Use a timeout of 300 seconds. If it times out, you should adjust the notebook and re-run.
7. If there are errors, fix them in the Jupytext `notebook.py` file, re-run the above command to convert and execute, repeating these steps until the notebook runs properly.

## Calling tools

In order to get information about the Dandiset and how to load data from NWB files within the Dandiset, you will need to use the following command-line tools:

```bash
dandi-notebook-gen-tools dandiset-info {{ DANDISET_ID }}
```

This will print the metadata of the Dandiset, including its name, description, and key metadata.

```bash
dandi-notebook-gen-tools dandiset-assets {{ DANDISET_ID }}
```

This will print the assets (files) available in the Dandiset. For each NWB file it will include the asset ID. From the asset ID you can construct the associated URL as follows:

https://api.dandiarchive.org/api/assets/{{ ASSET_ID }}/download/

```bash
dandi-notebook-gen-tools nwb-file-info {{ DANDISET_ID }} <NWB_FILE_URL>
```

This will print usage information on how to load data from the NWB file. Be sure to use the URL provided by this tool to load the NWB file.

It's very important that you use all of the above tools before you start creating the notebook so you understand the Dandiset, the data it contains, and how to load that data in Python.

# Exploring the NWB file

Create and execute python scripts in a tmp_scripts subdirectory. The scripts can generate text output and/or plots. The plots image files should also go in the tmp_scripts subdirectory. You should always use the read_image tool to read the image files for the plots you create.

to learn about the graphs that you create. This will help you know whether the graphs are informative enough to include in the notebook as well as information about the data that will help you make decisions and know how to describe things in the notebook. Both the script outputs and plots will help inform you about what to put in the notebook. Feel free to transform, process, and combine the data in common ways to make interesting, informative plots for a scientist to interpret. Feel free to run as many scripts as you need to gather the information required to make a good notebook. The more quality information you have, the better you will be able to do in making the notebook. Include comments at the top of each script explaining what information you are trying to obtain with the script.

IMPORTANT: Every good quality plot produced by the scripts should be included in the final notebook.

# About the notebook

Your resulting Jupytext should be educational, well-documented, and follow best practices for neurophysiology data analysis. Include comments in code cells to explain what each step does.

Prominently inform the user that the notebook was AI-generated using dandi-notebook-gen and has not been fully verified, and that they should be cautious when interpreting the code or results.

Assume that all the packages you would need are already installed on the user's system. The resulting Jupytext should not include instructions to run pip install (no code cells starting with "!"). The markdown cells should include instructions for the user to install any necessary packages.

The resulting Jupytext should include a code block at the start of the notebook that uses the DANDI API to list all of the assets in the Dandiset. This code block should look like:
# %%
from dandi.dandiapi import DandiAPIClient
client = DandiAPIClient()
dandiset = client.get_dandiset("{{ DANDISET_ID }}")
assets = list(dandiset.get_assets())

The resulting Jupytext should select an NWB file from the Dandiset that contains data that would be nice to visualize.

The Jupytext should use `# %% [markdown]` for markdown cells and `# %%` delimiters for the code cells.

## Some notes:

If you load data from only select files, then you should indicate which files you are using.

Note that it doesn't work to try to index an h5py.Dataset with a numpy array of indices.

Note that you cannot do operations like np.sum over a h5py.Dataset. You need to get a numpy array using something like dataset[:]

If you are going to load a subset of data, it doesn't make sense to load all of the timestamps in memory and then select a subset. Instead, you should load the timestamps for the subset of data you are interested in. So we shouldn't ever see something like `dataset.timestamps[:]` unless we intend to load all the timestamps.

When loading data for illustration, be careful about the size of the data, since the files are hosted remotely and datasets are streamed over the network. You may want to load subsets of data. But if you do, please be sure to indicate that you are doing so, so the reader doesn't get the wrong impression about the data.

Keep in mind that through your tool calls you have been given information about what data are available in the files, whereas the reader of the notebook does not have access to that information. So in your illustration it would be helpful to show how they could get that information (e.g., columns in a table, etc).

When showing unit IDs or channel IDs, be sure to use the actual IDs rather than just the indices.

When calling `lindi.LindiH5pyFile.from_lindi_file` you should not use the download URL directly, instead you should follow the instructions from the `nwb_file_info` tool which will have the appropriate URL to use and python commands to incorporate in the notebook.

`plt.style.use('seaborn')` is deprecated. If you want to use seaborn styling, use:
```
import seaborn as sns
sns.set_theme()
```
Do not use seaborn styling for plotting images.

Image masks values range from 0 to 1. If you are plotting all image masks superimposed on each other in a single figure, use a heatmap with np.max on the image masks.