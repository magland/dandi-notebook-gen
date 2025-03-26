"""
Tests for the logger module
"""

import os
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

from dandi_notebook_gen.logger import AILogger

def test_logger_init():
    """Test that the logger initializes correctly"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test with default log file name
        logger = AILogger(log_dir=tmpdir)
        assert logger.log_dir == Path(tmpdir)
        assert logger.log_path.parent == Path(tmpdir)
        assert logger.log_path.name.startswith("ai_log_")
        assert logger.log_path.name.endswith(".json")

        # Test with custom log file name
        custom_log_file = "custom_log.json"
        logger = AILogger(log_dir=tmpdir, log_file=custom_log_file)
        assert logger.log_dir == Path(tmpdir)
        assert logger.log_path == Path(tmpdir) / custom_log_file

def test_logger_file_creation():
    """Test that the logger creates the log file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = "test_log.json"
        logger = AILogger(log_dir=tmpdir, log_file=log_file)

        # Check that the log file was created
        log_path = Path(tmpdir) / log_file
        assert log_path.exists()

        # Check that the log file contains an empty array
        with open(log_path, 'r') as f:
            content = json.load(f)
            assert isinstance(content, list)
            assert len(content) == 0

def test_log_interaction():
    """Test that the logger can log an interaction"""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = "test_log.json"
        logger = AILogger(log_dir=tmpdir, log_file=log_file)

        # Sample data for logging
        input_messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello, world!"}
        ]
        output_content = "Hello! How can I assist you today?"
        conversation_messages = input_messages + [
            {"role": "assistant", "content": output_content}
        ]
        prompt_tokens = 100
        completion_tokens = 50
        model = "test-model"
        metadata = {"test_key": "test_value"}

        # Log the interaction
        logger.log_interaction(
            input_messages=input_messages,
            output_content=output_content,
            conversation_messages=conversation_messages,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model=model,
            metadata=metadata
        )

        # Check that the log file contains the expected data
        log_path = Path(tmpdir) / log_file
        with open(log_path, 'r') as f:
            logs = json.load(f)
            assert len(logs) == 1

            log_entry = logs[0]
            assert log_entry["model"] == model
            assert log_entry["input_messages"] == input_messages
            assert log_entry["output_content"] == output_content
            assert log_entry["conversation_messages"] == conversation_messages
            assert log_entry["token_usage"]["prompt_tokens"] == prompt_tokens
            assert log_entry["token_usage"]["completion_tokens"] == completion_tokens
            assert log_entry["token_usage"]["total_tokens"] == prompt_tokens + completion_tokens
            assert log_entry["metadata"] == metadata

            # Check that the timestamp is in ISO format
            assert "timestamp" in log_entry
            # This will raise an exception if the timestamp is not in ISO format
            datetime.fromisoformat(log_entry["timestamp"])

def test_multiple_log_entries():
    """Test that the logger can log multiple interactions"""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = "test_log.json"
        logger = AILogger(log_dir=tmpdir, log_file=log_file)

        # Log multiple interactions
        for i in range(3):
            logger.log_interaction(
                input_messages=[{"role": "user", "content": f"Message {i}"}],
                output_content=f"Response {i}",
                conversation_messages=[
                    {"role": "user", "content": f"Message {i}"},
                    {"role": "assistant", "content": f"Response {i}"}
                ],
                prompt_tokens=100 + i,
                completion_tokens=50 + i,
                model="test-model",
                metadata={"index": i}
            )

        # Check that the log file contains all entries
        log_path = Path(tmpdir) / log_file
        with open(log_path, 'r') as f:
            logs = json.load(f)
            assert len(logs) == 3

            for i, log_entry in enumerate(logs):
                assert log_entry["input_messages"][0]["content"] == f"Message {i}"
                assert log_entry["output_content"] == f"Response {i}"
                assert log_entry["metadata"]["index"] == i
