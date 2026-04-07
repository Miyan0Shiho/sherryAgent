"""
Benchmark runner with integrated execution logging.

Runs agent execution and logs complete process using ExecutionLogger.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from src.sherry_agent.execution.agent_loop import (
    agent_loop,
    ToolExecutor,
)
from src.sherry_agent.models.config import AgentConfig
from src.sherry_agent.models.events import AgentEvent, CancellationToken
from src.sherry_agent.llm.client import LLMClient

from .logger import ExecutionLogger


class LoggingToolExecutor(ToolExecutor):
    """Tool executor wrapper that logs tool calls."""
    
    def __init__(self, inner: ToolExecutor, logger: ExecutionLogger) -> None:
        self.inner = inner
        self.logger = logger
    
    async def execute_tool(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        call_id: str,
    ) -> tuple[str, dict[str, Any]]:
        """Execute tool and log the call."""
        self.logger.start_tool_call(tool_name, tool_input, call_id)
        
        try:
            result_content, result_metadata = await self.inner.execute_tool(
                tool_name,
                tool_input,
                call_id,
            )
            self.logger.end_tool_call(call_id, result_content, result_metadata)
            return result_content, result_metadata
        except Exception as e:
            self.logger.log_error(e, f"Tool execution failed: {tool_name}")
            self.logger.end_tool_call(
                call_id,
                f"Error: {str(e)}",
                {"error": str(e), "error_type": type(e).__name__},
            )
            raise


async def run_benchmark(
    messages: list[dict[str, Any]],
    config: AgentConfig,
    llm_client: LLMClient,
    tool_executor: ToolExecutor | None = None,
    cancellation_token: CancellationToken | None = None,
    log_dir: str | Path | None = None,
    task_id: str | None = None,
) -> dict[str, Any]:
    """
    Run agent execution with logging.
    
    Args:
        messages: Initial messages to send to the agent
        config: Agent configuration
        llm_client: LLM client instance
        tool_executor: Optional tool executor
        cancellation_token: Optional cancellation token
        log_dir: Directory to save logs (default: tests/benchmark/logs)
        task_id: Optional task identifier
    
    Returns:
        Execution summary dictionary
    """
    if log_dir is None:
        log_dir = Path(__file__).parent / "logs"
    
    if task_id is None:
        task_id = "benchmark_task"
    
    logger = ExecutionLogger(log_dir, run_id=None)
    logger.start_execution(task_id, {
        "model": config.model,
        "max_tool_rounds": config.max_tool_rounds,
        "token_budget": config.token_budget,
    })
    
    success = False
    events_collected: list[AgentEvent] = []
    
    try:
        wrapped_tool_executor: ToolExecutor | None = None
        if tool_executor:
            wrapped_tool_executor = LoggingToolExecutor(tool_executor, logger)
        
        event_iterator = agent_loop(
            messages=messages,
            config=config,
            llm_client=llm_client,
            tool_executor=wrapped_tool_executor,
            cancellation_token=cancellation_token,
        )
        
        async for event in logger.consume_events(event_iterator):
            events_collected.append(event)
        
        success = True
        summary = "Benchmark completed successfully"
        
    except Exception as e:
        logger.log_error(e, "Benchmark execution failed")
        summary = f"Benchmark failed: {str(e)}"
        raise
    
    finally:
        logger.end_execution(success, summary)
    
    final_summary = logger.get_summary()
    final_summary["events_collected"] = len(events_collected)
    
    return final_summary


def run_benchmark_sync(
    messages: list[dict[str, Any]],
    config: AgentConfig,
    llm_client: LLMClient,
    tool_executor: ToolExecutor | None = None,
    cancellation_token: CancellationToken | None = None,
    log_dir: str | Path | None = None,
    task_id: str | None = None,
) -> dict[str, Any]:
    """Synchronous wrapper for run_benchmark."""
    return asyncio.run(
        run_benchmark(
            messages=messages,
            config=config,
            llm_client=llm_client,
            tool_executor=tool_executor,
            cancellation_token=cancellation_token,
            log_dir=log_dir,
            task_id=task_id,
        )
    )
