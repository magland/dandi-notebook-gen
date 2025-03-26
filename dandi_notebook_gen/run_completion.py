from typing import Dict, Any, List, Optional, Tuple
import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

from .tools import dandiset_assets, nwb_file_info, dandiset_info
from .logger import AILogger

# Load environment variables from .env file
load_dotenv()

available_tools = [
    getattr(dandiset_info, "spec"),
    getattr(dandiset_assets, "spec"),
    getattr(nwb_file_info, "spec")
]

def run_completion(
    messages: List[Dict[str, Any]],
    *,
    model: str,
    log_dir: str = "logs",
    log_file: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Tuple[str, List[Dict[str, Any]], int, int]:
    """Execute an AI completion request using the OpenRouter API with support for tool calls.

    This function manages a conversation with an AI model, handling tool execution
    and response processing in a loop until a final response is received.

    Args:
        messages: List of conversation messages, each being a dictionary with role and content.
        model: Name of the OpenRouter model to use for completion.
        log_dir: Directory where log files will be stored, by default "logs"
        log_file: Name of the log file. If None, a timestamped filename will be generated.
        metadata: Additional metadata to include in the log entry.

    Returns:
        tuple: Contains:
            - content (str): The final response content from the model
            - conversation_messages (List): Complete conversation history including tool calls
            - total_prompt_tokens (int): Total tokens used in prompts
            - total_completion_tokens (int): Total tokens used in completions

    Raises:
        ValueError: If OPENROUTER_API_KEY environment variable is not set
        RuntimeError: If the OpenRouter API request fails
        json.JSONDecodeError: If tool arguments cannot be parsed

    Notes:

    The OPENROUTER_API_KEY environment variable must be set with a valid API key from OpenRouter.

    The messages is a list of dicts with the following structure:
    [
        {"role": "system", "content": "You are a helpful assistant... etc."},
        {"role": "user", "content": "I need help with... etc."},
        {"role": "assistant", "content": "I can help with that... etc."},
        {"role": "user", "content": "Yes, please... etc."},
        ...
    ]
    """
    # Initialize the logger
    logger = AILogger(log_dir=log_dir, log_file=log_file)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://neurosift.app",
        "Content-Type": "application/json"
    }

    conversation_messages = [m for m in messages]

    total_prompt_tokens = 0
    total_completion_tokens = 0

    while True:
        # Make API request
        payload = {
            "model": model,
            "messages": conversation_messages,
            # "max_tokens": 1000,
            "tools": available_tools,
            "tool_choice": "auto"
        }
        print(f"Using model: {payload['model']}")
        print(f"Num. messages in conversation: {len(conversation_messages)}")

        print("Submitting completion request...")
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter API request failed: {response.text}")

        print("Processing response...")
        completion = response.json()
        promt_tokens = completion["usage"]["prompt_tokens"]
        completion_tokens = completion["usage"]["completion_tokens"]
        total_prompt_tokens += promt_tokens
        total_completion_tokens += completion_tokens
        print(f'TOKENS: {int(promt_tokens / 100) / 10} prompt, {int(completion_tokens / 100) / 10} completion; total: {int(total_prompt_tokens / 100) / 10} prompt, {int(total_completion_tokens / 100) / 10} completion')

        message = completion["choices"][0]["message"]
        content = message.get("content", "")
        tool_calls = message.get("tool_calls", [])

        print("\nReceived assistant response...")
        print(f'Tool calls: {[tc["function"]["name"] for tc in tool_calls]}')
        # Track assistant response
        current_response = {
            "role": "assistant",
            "content": content
        }
        if tool_calls:
            current_response["tool_calls"] = tool_calls
        conversation_messages.append(current_response)

        if tool_calls:
            # Handle each tool call
            for tool_call in tool_calls:
                if tool_call["type"] != "function":
                    continue

                tool_name = tool_call["function"]["name"]
                try:
                    tool_args = json.loads(tool_call["function"]["arguments"])
                except json.JSONDecodeError:
                    print(f"Failed to parse tool arguments for {tool_name}")
                    print(tool_call)
                    raise

                print(f"\nExecuting tool: {tool_name} with args: {tool_args}")
                # Execute the tool
                tool_result = {}
                if tool_name == "dandiset_info":
                    tool_result = dandiset_info(**tool_args)
                elif tool_name == "dandiset_assets":
                    tool_result = dandiset_assets(**tool_args)
                elif tool_name == "nwb_file_info":
                    tool_result = nwb_file_info(**tool_args)
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

                tool_response = {
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(tool_result),
                    "tool_call_id": tool_call["id"]
                }
                conversation_messages.append(tool_response)
        else:
            # Log the interaction
            logger.log_interaction(
                input_messages=messages,
                output_content=content,
                conversation_messages=conversation_messages,
                prompt_tokens=total_prompt_tokens,
                completion_tokens=total_completion_tokens,
                model=model,
                metadata=metadata
            )

            return content, conversation_messages, total_prompt_tokens, total_completion_tokens
