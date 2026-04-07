
"""Benchmark test suite for SherryAgent."""

from __future__ import annotations

from typing import Any

__version__ = "0.1.0"

__all__ = [
    "ExecutionLogger",
    "LogEntry",
    "ToolCallLog",
    "LogEventType",
    "run_benchmark",
    "run_benchmark_sync",
    "LoggingToolExecutor",
    "PerformanceBenchmark",
    "MemoryBenchmark",
    "LLMBenchmark",
    "ConcurrencyBenchmark",
    "run_full_benchmark_suite",
]


def __getattr__(name: str) -> Any:
    if name == "ExecutionLogger":
        from .logger import ExecutionLogger
        return ExecutionLogger
    elif name == "LogEntry":
        from .logger import LogEntry
        return LogEntry
    elif name == "ToolCallLog":
        from .logger import ToolCallLog
        return ToolCallLog
    elif name == "LogEventType":
        from .logger import LogEventType
        return LogEventType
    elif name == "run_benchmark":
        from .benchmark_runner import run_benchmark
        return run_benchmark
    elif name == "run_benchmark_sync":
        from .benchmark_runner import run_benchmark_sync
        return run_benchmark_sync
    elif name == "LoggingToolExecutor":
        from .benchmark_runner import LoggingToolExecutor
        return LoggingToolExecutor
    elif name == "PerformanceBenchmark":
        from .performance_benchmark import PerformanceBenchmark
        return PerformanceBenchmark
    elif name == "MemoryBenchmark":
        from .performance_benchmark import MemoryBenchmark
        return MemoryBenchmark
    elif name == "LLMBenchmark":
        from .performance_benchmark import LLMBenchmark
        return LLMBenchmark
    elif name == "ConcurrencyBenchmark":
        from .performance_benchmark import ConcurrencyBenchmark
        return ConcurrencyBenchmark
    elif name == "run_full_benchmark_suite":
        from .performance_benchmark import run_full_benchmark_suite
        return run_full_benchmark_suite
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


