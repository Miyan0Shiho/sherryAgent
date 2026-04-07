"""
Tests for the benchmark execution logger.
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime
import pytest

from src.sherry_agent.models.events import AgentEvent, EventType, TokenUsage

from tests.benchmark.logger import (
    ExecutionLogger,
    LogEntry,
    ToolCallLog,
    LogEventType,
)


def test_log_entry_to_dict():
    """Test converting LogEntry to dict."""
    entry = LogEntry(
        timestamp="2024-01-01T00:00:00",
        event_type="text",
        content="Hello, world!",
        metadata={"key": "value"},
        token_usage={"input_tokens": 100, "output_tokens": 200},
    )
    entry_dict = entry.to_dict()
    
    assert entry_dict["timestamp"] == "2024-01-01T00:00:00"
    assert entry_dict["event_type"] == "text"
    assert entry_dict["content"] == "Hello, world!"
    assert entry_dict["metadata"] == {"key": "value"}
    assert entry_dict["token_usage"] == {"input_tokens": 100, "output_tokens": 200}


def test_log_entry_to_json():
    """Test converting LogEntry to JSON."""
    entry = LogEntry(
        timestamp="2024-01-01T00:00:00",
        event_type="text",
        content="Hello, world!",
    )
    json_str = entry.to_json()
    parsed = json.loads(json_str)
    
    assert parsed["timestamp"] == "2024-01-01T00:00:00"
    assert parsed["event_type"] == "text"
    assert parsed["content"] == "Hello, world!"


def test_log_entry_to_human_readable():
    """Test converting LogEntry to human-readable format."""
    entry = LogEntry(
        timestamp="2024-01-01T00:00:00",
        event_type="text",
        content="Hello, world!",
        metadata={"key": "value"},
    )
    readable = entry.to_human_readable()
    
    assert "[2024-01-01T00:00:00]" in readable
    assert "TEXT" in readable
    assert "Hello, world!" in readable
    assert '"key": "value"' in readable


def test_tool_call_log_complete():
    """Test completing a tool call log."""
    tool_call = ToolCallLog(
        tool_name="test_tool",
        tool_input={"param": "value"},
        call_id="call_123",
        start_time=1000.0,
    )
    
    tool_call.complete("Result content", {"status": "success"})
    
    assert tool_call.end_time is not None
    assert tool_call.duration_ms is not None
    assert tool_call.result_content == "Result content"
    assert tool_call.result_metadata == {"status": "success"}


def test_execution_logger_basic():
    """Test basic ExecutionLogger functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir)
        logger = ExecutionLogger(log_dir, run_id="test_run")
        
        assert logger.run_id == "test_run"
        assert logger.json_log_path.name == "test_run.jsonl"
        assert logger.text_log_path.name == "test_run.log"
        assert log_dir.exists()


def test_execution_logger_start_end():
    """Test starting and ending execution."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir)
        logger = ExecutionLogger(log_dir, run_id="test_run")
        
        logger.start_execution("test_task", {"config_key": "config_value"})
        logger.end_execution(True, "All done!")
        
        assert logger.start_time is not None
        assert logger.end_time is not None
        assert len(logger.entries) == 2
        
        summary = logger.get_summary()
        assert summary["run_id"] == "test_run"
        assert summary["success"] is True


def test_execution_logger_log_event():
    """Test logging AgentEvent."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir)
        logger = ExecutionLogger(log_dir, run_id="test_run")
        
        event = AgentEvent(
            event_type=EventType.TEXT,
            content="Test message",
            token_usage=TokenUsage(input_tokens=50, output_tokens=100),
        )
        
        logger.log_event(event)
        
        assert len(logger.entries) == 1
        assert logger.total_tokens == 150


def test_execution_logger_tool_calls():
    """Test logging tool calls."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir)
        logger = ExecutionLogger(log_dir, run_id="test_run")
        
        logger.start_tool_call("my_tool", {"x": 1, "y": 2}, "call_456")
        logger.end_tool_call("call_456", "Tool result", {"result": 3})
        
        assert "call_456" in logger.tool_calls
        tool_call = logger.tool_calls["call_456"]
        assert tool_call.tool_name == "my_tool"
        assert tool_call.tool_input == {"x": 1, "y": 2}
        assert tool_call.result_content == "Tool result"


def test_execution_logger_error():
    """Test logging errors."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir)
        logger = ExecutionLogger(log_dir, run_id="test_run")
        
        try:
            raise ValueError("Test error")
        except ValueError as e:
            logger.log_error(e, "Test context")
        
        assert len(logger.entries) == 1
        entry = logger.entries[0]
        assert entry.event_type == "error"
        assert "Test error" in entry.content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
