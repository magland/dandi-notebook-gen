# Neuroscience Phenomenon Demonstration Instructions

You are going to create a Jupytext notebook called `notebook.py` that will demonstrate a specific scientific finding in systems neuroscience: {{ PHENOMENON }}. The notebook will use data from a relevant Dandiset to provide clear visualizations and analyses showing this phenomenon. After you create the notebook, convert it to `notebook.ipynb` and execute the Jupyter notebook to make sure it runs without errors. If there are errors, you will need to fix them in the original `notebook.py` file, re-convert and re-run the notebook, repeating until it runs properly.

The notebook should:

1. Provide an introduction to the {{ PHENOMENON }} phenomenon, including its scientific significance and key characteristics
2. Find and select an appropriate Dandiset that contains data suitable for demonstrating this phenomenon
3. Include code to load and explore the dataset's structure
4. Demonstrate how to access and visualize the specific data that shows the {{ PHENOMENON }} phenomenon
5. Include explanatory markdown cells that guide the user through the analysis process and highlight the key aspects of the phenomenon
6. Provide quantitative analyses that support and characterize the phenomenon

Important:
1. Do not simulate the data! If the chosen dandiset is not working, try another dandiset. Try three different dandisets before giving up. THIS IS IMPORTANT! DO NOT SIMULATE DATA!
2. Where possible, show trial-wise visualizations such as raster + psth to demonstrate the phenomenon.
3. When creating summary plots, use SEM error bars and include the appropriate statistics for making conclusions about significance.

Here's the plan that you should follow:
1. Use `dandi-notebook-gen-tools dandi-search` or `dandi-notebook-gen-tools dandi-semantic-search` to find datasets that might contain data relevant to {{ PHENOMENON }}.
2. Select a promising Dandiset and get its metadata using `dandi-notebook-gen-tools dandiset-info <DANDISET_ID>`.
3. Get the Dandiset assets using `dandi-notebook-gen-tools dandiset-assets <DANDISET_ID>`.
4. Choose an NWB file from the assets and get its information using `dandi-notebook-gen-tools nwb-file-info <DANDISET_ID> <NWB_FILE_URL>`.
5. Do exploratory research on the contents of the Dandiset by creating and executing python scripts in a tmp_scripts subdirectory to generate text output and plots focused on identifying and demonstrating the {{ PHENOMENON }} phenomenon.
  - It's very important that the plots go to .PNG image files in the tmp_scripts subdirectory. Otherwise, if the plot is displayed in a window, the script will hang. So do not do a plt.show().
  - If the script times out (use a timeout of 90 seconds for the scripts), you may be trying to load too much data. Try revising the script and rerun.
  - After executing each script, if you created plots, always review each plot using the read_image tool to be able to gain information about them. Each call to read_image should include instructions that give context for the image and that help determine whether the plot shows evidence of the {{ PHENOMENON }} phenomenon.
6. Write the content of the notebook to `notebook.py`, including the introduction to the phenomenon, dataset selection rationale, data analysis, and clear visualizations that demonstrate the {{ PHENOMENON }}.
7. Run `jupytext --to notebook notebook.py && jupyter execute --inplace notebook.ipynb` to convert the notebook to a Jupyter notebook and execute the resulting `notebook.ipynb` to make sure it runs without errors and produces output cells. Use a timeout of 600 seconds. If it times out, you should adjust the notebook and re-run.
8. If there are errors, fix them in the Jupytext `notebook.py` file, re-run the above command to convert and execute, repeating these steps until the notebook runs properly.

## Be careful about drawing conclusions

The purpose of this notebook is to demonstrate a specific scientific phenomenon using real neuroscience data. While you should highlight the key features that characterize the phenomenon, it's important that you avoid making claims that are not supported by the appropriate statistical tests. The AI summary of plots in the read_image tool can sometimes hallucinate and report trends in the data that are not statistically significant, which is something you should be aware of. You may want to instruct the read_image tool to be careful about this. If there are obvious and apparent features of plots that are consistent with the known characteristics of the phenomenon, then it is appropriate to point them out. But be mindful of the limitations and avoid overinterpreting the data.

When summarizing the notebook, make sure your claims about the phenomenon are supported by the data and analyses you've performed. Focus on clear demonstrations rather than novel scientific conclusions.

## Calling tools

In order to find an appropriate dataset and understand how to load data from NWB files, you will need to use the following command-line tools:

```bash
dandi-notebook-gen-tools dandi-search "<search_query>"
```

This will search for datasets in the DANDI archive using keywords. Craft your search query to find datasets likely to contain data that can demonstrate the {{ PHENOMENON }} phenomenon.

```bash
dandi-notebook-gen-tools dandi-semantic-search "<natural_language_query>"
```

This will perform a semantic search using natural language to find relevant datasets. Use this to describe the type of data you're looking for to demonstrate the {{ PHENOMENON }} phenomenon.

```bash
dandi-notebook-gen-tools dandiset-info <DANDISET_ID>
```

This will print the metadata of the Dandiset, including its name, description, and key metadata.

```bash
dandi-notebook-gen-tools dandiset-assets <DANDISET_ID>
```

This will print the assets (files) available in the Dandiset. For each NWB file it will include the asset ID. From the asset ID you can construct the associated URL as follows:

https://api.dandiarchive.org/api/assets/<ASSET_ID>/download/

```bash
dandi-notebook-gen-tools nwb-file-info <DANDISET_ID> <NWB_FILE_URL>
```

This will print usage information on how to load data from the NWB file. Be sure to use the URL provided by this tool to load the NWB file.

It's very important that you use all of the above tools to first find an appropriate dataset and then understand its contents before you start creating the notebook.

# Exploring the NWB file

Create and execute python scripts in a tmp_scripts subdirectory. The scripts should focus on generating text output and plots that specifically demonstrate the {{ PHENOMENON }} phenomenon. The plots image files should go in the tmp_scripts subdirectory. You should always use the read_image tool to read the image files for the plots you create.

Focus your exploration on finding clear examples of the requested phenomenon. This may require specialized analyses depending on the phenomenon.

Include comments at the top of each script explaining what aspect of the phenomenon you are trying to demonstrate with the script.

IMPORTANT: Every high-quality plot that successfully demonstrates the {{ PHENOMENON }} should be included in the final notebook.

# About the notebook

Your resulting Jupytext should be educational, well-documented, and focus on clearly demonstrating the requested phenomenon. The notebook should:

1. Start with a thorough introduction to the {{ PHENOMENON }}, including its scientific context, discovery history, and significance
2. Clearly explain why the selected dataset is appropriate for demonstrating this phenomenon
3. Include well-commented code that processes and analyzes the data to reveal the phenomenon (do not simulate data)
4. Feature clear visualizations that highlight the key characteristics of the phenomenon
5. Include quantitative analyses that support the demonstration (e.g., tuning curves, statistical measures)
6. Discuss how the results from this dataset compare to the established understanding of the phenomenon

Prominently inform the user that the notebook was AI-generated using dandi-notebook-gen and has not been fully verified, and that they should be cautious when interpreting the code or results.

Assume that all the packages you would need are already installed on the user's system. The resulting Jupytext should not include instructions to run pip install (no code cells starting with "!"). The markdown cells should include instructions for the user to install any necessary packages.

The resulting Jupytext should include a code block near the start of the notebook that uses the DANDI API to access the selected Dandiset:
# %%
from dandi.dandiapi import DandiAPIClient
client = DandiAPIClient()
dandiset = client.get_dandiset("<DANDISET_ID>")
assets = list(dandiset.get_assets())

The Jupytext should use `# %% [markdown]` for markdown cells and `# %%` delimiters for the code cells.

## Some notes

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