"""
Logger for AI inputs and outputs in JSON format
"""

import json
import os
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

class AILogger:
    """
    Logger for AI inputs and outputs in JSON format.

    This class provides functionality to log AI interactions (inputs and outputs)
    to a JSON file. Each log entry includes timestamps, messages, token usage,
    and other relevant information.
    """

    def __init__(self, log_dir: str = "logs", log_file: Optional[str] = None):
        """
        Initialize the logger.

        Parameters
        ----------
        log_dir : str, optional
            Directory where log files will be stored, by default "logs"
        log_file : str, optional
            Name of the log file. If None, a timestamped filename will be generated.
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)

        if log_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"ai_log_{timestamp}.json"

        self.log_path = self.log_dir / log_file

        # Initialize log file with an empty array if it doesn't exist
        if not self.log_path.exists():
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def log_interaction(self,
                        input_messages: List[Dict[str, Any]],
                        output_content: str,
                        conversation_messages: List[Dict[str, Any]],
                        prompt_tokens: int,
                        completion_tokens: int,
                        model: str,
                        metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an AI interaction.

        Parameters
        ----------
        input_messages : List[Dict[str, Any]]
            The input messages sent to the AI.
        output_content : str
            The final output content from the AI.
        conversation_messages : List[Dict[str, Any]]
            The complete conversation history including tool calls.
        prompt_tokens : int
            Number of tokens used in the prompt.
        completion_tokens : int
            Number of tokens used in the completion.
        model : str
            The AI model used for the interaction.
        metadata : Dict[str, Any], optional
            Additional metadata to include in the log entry.
        """
        timestamp = datetime.datetime.now().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "model": model,
            "input_messages": input_messages,
            "output_content": output_content,
            "conversation_messages": conversation_messages,
            "token_usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        }

        if metadata:
            log_entry["metadata"] = metadata

        # Read existing logs
        with open(self.log_path, 'r') as f:
            logs = json.load(f)

        # Append new log entry
        logs.append(log_entry)

        # Write updated logs
        with open(self.log_path, 'w') as f:
            json.dump(logs, f, indent=2)

        print(f"Logged AI interaction to {self.log_path}")

    def get_log_path(self) -> Path:
        """
        Get the path to the log file.

        Returns
        -------
        Path
            Path to the log file.
        """
        return self.log_path
