# Notebook Generation Instructions

You are going to create a Jupytext notebook called notebook.py that will help researchers explore and analyze a Dandiset {{ DANDISET_ID }}. After you create the notebook, execute it using `python notebook.py` to make sure it runs without errors. If there are errors, you will need to fix them and then re-run the notebook, repeating until it runs properly.

The notebook should

1. Provide an introduction to the Dandiset, including its name, description, and key metadata
2. Include code to load and explore the dataset's structure
3. Demonstrate how to access and visualize sample data from NWB files
4. Include explanatory markdown cells that guide the user through the analysis process
5. Provide examples of common analyses that might be relevant to the dataset's content

## Calling tools

In order to get information about the Dandiset and how to load data from NWB files within the Dandiset, you will need to use the following command-line tools:

```bash
dandi-notebook-gen-tools dandiset-info <DANDISET_ID>
```

This will print the metadata of the Dandiset, including its name, description, and key metadata.

```bash
dandi-notebook-gen-tools dandiset-assets <DANDISET_ID>
```

This will print the assets (files) available in the Dandiset. For each NWB file it will include a URL that can be passed into the nwb-file-info tool.

```bash
dandi-notebook-gen-tools nwb-file-info <DANDISET_ID> <NWB_FILE_URL>
```

This will print usage information on how to load data from the NWB file.

It's very important that you use all of the above tools before you start creating the notebook so you understand the Dandiset, the data it contains, and how to load that data in Python.

# About the notebook

Your resulting Jupytext should be educational, well-documented, and follow best practices for neurophysiology data analysis. Include comments in code cells to explain what each step does.

The resulting Jupytext should not include instructions to run pip install (no code cells starting with "!"). The markdown cells should include instructions for the user to install any necessary packages.

The resulting Jupytext should include a code block at the start of the notebook that uses the DANDI API to list all of the assets in the Dandiset. This code block should look like:
# %%
from dandi.dandiapi import DandiAPIClient
client = DandiAPIClient()
dandiset_id = "000000"
dandiset = client.get_dandiset(dandiset_id)
assets = list(dandiset.get_assets())

But the `dandiset_id` should be the actual ID of the Dandiset you are working with.

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

When calling `lindi.LindiH5pyFile.from_lindi_file` with a URL, the URL should be a nwb.lindi.json file which should come from the nwb-file-info tool. It should NOT be a download URL to the NWB file from api.dandiarchive.org.
