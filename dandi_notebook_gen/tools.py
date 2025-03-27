from typing import Dict, Any, Optional
import requests
import os
import base64

def dandiset_assets(
    dandiset_id: str,
    version: str = "draft",
    page: int = 1,
    page_size: int = 20,
    glob: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a list of assets/files in a dandiset version.

    The output provides:
    - count: total number of assets
    - results: array of assets with asset_id, path, and size

    Parameters
    ----------
    dandiset_id : str
        DANDI dataset ID
    version : str, optional
        Version of the dataset to retrieve, by default "draft"
    page : int, optional
        Page number, by default 1
    page_size : int, optional
        Number of results per page, by default 20
    glob : str, optional
        Optional glob pattern to filter files (e.g., '*.nwb' for NWB files)

    Returns
    -------
    Dict[str, Any]
        Dictionary containing count and results
    """
    url = "https://neurosift-chat-agent-tools.vercel.app/api/dandiset_assets"
    payload = {
        "dandiset_id": dandiset_id,
        "version": version,
        "page": page,
        "page_size": page_size,
    }
    if glob:
        payload["glob"] = glob

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch dandiset assets: {response.text}")
    return response.json()

def nwb_file_info(dandiset_id: str, nwb_file_url: str) -> Dict[str, Any]:
    """Get information about an NWB file.

    Includes metadata and information about how to load the neurodata objects
    using pynwb and lindi.

    Parameters
    ----------
    dandiset_id : str
        DANDI dataset ID
    nwb_file_url : str
        URL of the NWB file in the DANDI archive

    Returns
    -------
    Dict[str, Any]
        Dictionary containing NWB file information
    """
    url = "https://neurosift-chat-agent-tools.vercel.app/api/nwb_file_info"
    payload = {"dandiset_id": dandiset_id, "nwb_file_url": nwb_file_url}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch NWB file info: {response.text}")
    return response.json()

def dandiset_info(dandiset_id: str, version: str = "draft") -> Dict[str, Any]:
    """Get information about a specific version of a DANDI dataset.

    When the version is unknown, use "draft".

    This will return detailed information about the dandiset including:
    name, description, access, license, citation, keywords, protocol,
    contributor names, date created, size, number of files, number of
    subjects, variables measured, and measurement technique.

    Parameters
    ----------
    dandiset_id : str
        DANDI dataset ID
    version : str, optional
        Version of the dataset to retrieve, by default "draft"

    Returns
    -------
    Dict[str, Any]
        Dictionary containing detailed dataset information
    """
    url = "https://neurosift-chat-agent-tools.vercel.app/api/dandiset_info"
    payload = {"dandiset_id": dandiset_id, "version": version}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch dandiset info: {response.text}")
    return response.json()

dandiset_info_spec = {
    "type": "function",
    "function": {
        "name": "dandiset_info",
        "description": """Get information about a specific version of a DANDI dataset.

When the version is unknown, use "draft".

This will return detailed information about the dandiset including:
name, description, access, license, citation, keywords, protocol, contributor names, date created, size, number of files, number of subjects, variables measured, and measurement technique.
""",
        "parameters": {
            "type": "object",
            "properties": {
                "dandiset_id": {"type": "string", "description": "DANDI dataset ID"},
                "version": {
                    "type": "string",
                    "description": "Version of the dataset (optional, defaults to 'draft')",
                },
            },
            "required": ["dandiset_id"],
        },
    },
}
setattr(dandiset_info, "spec", dandiset_info_spec)

dandiset_assets_spec = {
    "type": "function",
    "function": {
        "name": "dandiset_assets",
        "description": """Get a list of assets/files in a dandiset version.

The output provides:
- count: total number of assets
- results: array of assets with asset_id, path, and size

The URL for the asset can be constructed as follows:
https://api.dandiarchive.org/api/assets/<asset_id>/download/

where XXXXXX is the dandiset ID and XXXXX is the version.""",
        "parameters": {
            "type": "object",
            "properties": {
                "dandiset_id": {"type": "string", "description": "DANDI dataset ID"},
                "version": {
                    "type": "string",
                    "description": "Version of the dataset (optional)",
                },
                "page": {"type": "integer", "description": "Page number (optional)"},
                "page_size": {
                    "type": "integer",
                    "description": "Results per page (optional)",
                },
                "glob": {
                    "type": "string",
                    "description": "File pattern filter (optional)",
                },
            },
            "required": ["dandiset_id"],
        },
    },
}
setattr(dandiset_assets, "spec", dandiset_assets_spec)

nwb_file_info_spec = {
    "type": "function",
    "function": {
        "name": "nwb_file_info",
        "description": """Get information about an NWB file, including metadata and information about how to load the neurodata objects using pynwb and lindi.

Be careful not to load too much data at once, as it can be slow and use a lot of memory.
""",
        "parameters": {
            "type": "object",
            "properties": {
                "dandiset_id": {"type": "string", "description": "DANDI dataset ID"},
                "nwb_file_url": {
                    "type": "string",
                    "description": "URL of the NWB file in DANDI",
                },
            },
            "required": ["dandiset_id", "nwb_file_url"],
        },
    },
}
setattr(nwb_file_info, "spec", nwb_file_info_spec)

def analyze_plot(image_path: str, additional_instructions: Optional[str] = None) -> Dict[str, Any]:
    """Analyze a scientific plot using the OpenRouter API with GPT-4V.

    This function reads an image file containing a scientific plot,
    converts it to base64, and uses OpenRouter's API with GPT-4V to
    generate a detailed description and analysis of the plot.

    Parameters
    ----------
    image_path : str
        Path to the image file (PNG format recommended)
    additional_instructions : str, optional
        Additional instructions to include in the system prompt

    Returns
    -------
    Dict[str, Any]
        Dictionary containing the analysis text in the 'text' field

    Raises
    ------
    RuntimeError
        If the API request fails or if OPENROUTER_API_KEY is not set
    FileNotFoundError
        If the image file does not exist
    """
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is required")

    with open(image_path, 'rb') as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    system_prompt = f"You are an expert at analyzing scientific plots. Your responses will be used by an AI system to understand whether plots are informative and what information they convey.\n{additional_instructions or ''}"

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please provide a detailed description and analysis of the plot in the image below."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        json=payload,
        headers={
            'Authorization': f'Bearer {api_key}',
            'HTTP-Referer': 'https://neurosift.app',
            'Content-Type': 'application/json'
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"Failed to analyze plot: {response.text}")

    result = response.json()
    return {"text": result['choices'][0]['message']['content']}

analyze_plot_spec = {
    "type": "function",
    "function": {
        "name": "analyze_plot",
        "description": """Analyze a scientific plot using the OpenRouter API with GPT-4V.

This function reads an image file containing a scientific plot and uses OpenRouter's API with GPT-4V vision model to generate a detailed description and analysis of the plot content.""",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file (PNG format recommended)"
                },
                "additional_instructions": {
                    "type": "string",
                    "description": "Additional instructions to include in the system prompt (optional)"
                }
            },
            "required": ["image_path"]
        }
    }
}
setattr(analyze_plot, "spec", analyze_plot_spec)
