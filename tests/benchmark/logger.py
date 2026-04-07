"""
Benchmark execution logger.

Records complete execution process with structured JSON and human-readable text formats.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from collections.abc import AsyncIterator

from src.sherry_agent.models.events import AgentEvent, EventType, TokenUsage


class LogEventType(Enum):
    """Event types for logging."""
    TEXT = "text"
    TOOL_USE = "tool_use"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    THINKING = "thinking"
    MEMORY_TRANSFER = "memory_transfer"
    EXECUTION_START = "execution_start"
    EXECUTION_END = "execution_end"


@dataclass
class ToolCallLog:
    """Detailed tool call log entry."""
    tool_name: str
    tool_input: dict[str, Any]
    call_id: str
    start_time: float
    end_time: float | None = None
    duration_ms: float | None = None
    result_content: str | None = None
    result_metadata: dict[str, Any] | None = None

    def complete(self, result_content: str, result_metadata: dict[str, Any]) -> None:
        """Mark tool call as complete with result."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        self.result_content = result_content
        self.result_metadata = result_metadata


@dataclass
class LogEntry:
    """Single log entry."""
    timestamp: str
    event_type: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    token_usage: dict[str, int] | None = None
    tool_call: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_human_readable(self) -> str:
        """Convert to human-readable string."""
        lines = [f"[{self.timestamp}] {self.event_type.upper()}"]
        
        if self.content:
            lines.append(f"  Content: {self.content}")
        
        if self.metadata:
            lines.append(f"  Metadata: {json.dumps(self.metadata, ensure_ascii=False, indent=2)}")
        
        if self.token_usage:
            lines.append(f"  Token Usage: {json.dumps(self.token_usage, ensure_ascii=False)}")
        
        if self.tool_call:
            lines.append(f"  Tool Call: {json.dumps(self.tool_call, ensure_ascii=False, indent=2)}")
        
        return "\n".join(lines)


class ExecutionLogger:
    """Logger for recording complete execution process."""

    def __init__(self, log_dir: str | Path, run_id: str | None = None) -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        if run_id is None:
            run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.run_id = run_id
        self.json_log_path = self.log_dir / f"{run_id}.jsonl"
        self.text_log_path = self.log_dir / f"{run_id}.log"
        
        self.entries: list[LogEntry] = []
        self.total_tokens: int = 0
        self.tool_calls: dict[str, ToolCallLog] = {}
        self.start_time: float | None = None
        self.end_time: float | None = None

    def _get_timestamp(self) -> str:
        """Get ISO format timestamp."""
        return datetime.now().isoformat()

    def _append_entry(self, entry: LogEntry) -> None:
        """Append entry to memory and files."""
        self.entries.append(entry)
        
        with open(self.json_log_path, "a", encoding="utf-8") as f:
            f.write(entry.to_json() + "\n")
        
        with open(self.text_log_path, "a", encoding="utf-8") as f:
            f.write(entry.to_human_readable() + "\n\n")

    def start_execution(self, task_id: str, config: dict[str, Any] | None = None) -> None:
        """Start logging execution."""
        self.start_time = time.time()
        
        entry = LogEntry(
            timestamp=self._get_timestamp(),
            event_type=LogEventType.EXECUTION_START.value,
            content=f"Execution started for task: {task_id}",
            metadata={
                "task_id": task_id,
                "config": config or {},
                "run_id": self.run_id,
            },
        )
        self._append_entry(entry)

    def end_execution(self, success: bool, summary: str | None = None) -> None:
        """End logging execution."""
        self.end_time = time.time()
        duration_ms = (self.end_time - self.start_time) * 1000 if self.start_time else 0
        
        entry = LogEntry(
            timestamp=self._get_timestamp(),
            event_type=LogEventType.EXECUTION_END.value,
            content=summary or "Execution completed",
            metadata={
                "success": success,
                "duration_ms": duration_ms,
                "total_tokens": self.total_tokens,
                "total_tool_calls": len(self.tool_calls),
            },
        )
        self._append_entry(entry)

    def log_event(self, event: AgentEvent) -> None:
        """Log an AgentEvent."""
        token_usage_dict = None
        if event.token_usage:
            token_usage_dict = {
                "input_tokens": event.token_usage.input_tokens,
                "output_tokens": event.token_usage.output_tokens,
                "cache_read_tokens": event.token_usage.cache_read_tokens,
                "cache_creation_tokens": event.token_usage.cache_creation_tokens,
            }
            self.total_tokens += sum(token_usage_dict.values())
        
        entry = LogEntry(
            timestamp=self._get_timestamp(),
            event_type=event.event_type.value,
            content=event.content,
            metadata=event.metadata,
            token_usage=token_usage_dict,
        )
        self._append_entry(entry)

    def start_tool_call(self, tool_name: str, tool_input: dict[str, Any], call_id: str) -> None:
        """Start logging a tool call."""
        tool_call = ToolCallLog(
            tool_name=tool_name,
            tool_input=tool_input,
            call_id=call_id,
            start_time=time.time(),
        )
        self.tool_calls[call_id] = tool_call

    def end_tool_call(self, call_id: str, result_content: str, result_metadata: dict[str, Any]) -> None:
        """End logging a tool call with result."""
        if call_id not in self.tool_calls:
            return
        
        tool_call = self.tool_calls[call_id]
        tool_call.complete(result_content, result_metadata)
        
        entry = LogEntry(
            timestamp=self._get_timestamp(),
            event_type=LogEventType.TOOL_RESULT.value,
            content=result_content,
            metadata=result_metadata,
            tool_call=asdict(tool_call),
        )
        self._append_entry(entry)

    def log_error(self, error: Exception, context: str | None = None) -> None:
        """Log an error."""
        entry = LogEntry(
            timestamp=self._get_timestamp(),
            event_type=LogEventType.ERROR.value,
            content=str(error),
            metadata={
                "context": context or "",
                "error_type": type(error).__name__,
            },
        )
        self._append_entry(entry)

    def get_summary(self) -> dict[str, Any]:
        """Get execution summary."""
        duration_ms = 0.0
        if self.start_time and self.end_time:
            duration_ms = (self.end_time - self.start_time) * 1000
        
        tool_durations = [
            tc.duration_ms for tc in self.tool_calls.values()
            if tc.duration_ms is not None
        ]
        
        avg_tool_duration = sum(tool_durations) / len(tool_durations) if tool_durations else 0
        
        return {
            "run_id": self.run_id,
            "duration_ms": duration_ms,
            "total_tokens": self.total_tokens,
            "total_tool_calls": len(self.tool_calls),
            "avg_tool_duration_ms": avg_tool_duration,
            "success": self.end_time is not None,
        }

    async def consume_events(self, event_iterator: AsyncIterator[AgentEvent]) -> AsyncIterator[AgentEvent]:
        """Consume and log events from an iterator."""
        try:
            async for event in event_iterator:
                self.log_event(event)
                yield event
        except Exception as e:
            self.log_error(e, "Error during event consumption")
            raise
