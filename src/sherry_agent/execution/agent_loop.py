"""Agent loop module for SherryAgent execution layer."""

import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

from ..infrastructure.concurrency import ConcurrencyManager
from ..llm.client import LLMClient
from ..memory.bridge import MemoryBridge
from ..memory.long_term import LongTermMemory
from ..memory.short_term import ShortTermMemory
from ..models.config import AgentConfig
from ..models.events import AgentEvent, CancellationToken, EventType, TokenUsage, ToolCall


class ToolExecutor(ABC):
    """Abstract base class for tool executors."""

    @abstractmethod
    async def execute_tool(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        call_id: str,
    ) -> tuple[str, dict[str, Any]]:
        """Execute a tool with the given parameters.

        Args:
            tool_name: Name of the tool to execute.
            tool_input: Input parameters for the tool.
            call_id: Unique identifier for this tool call.

        Returns:
            Tuple of (result_content, result_metadata).
        """
        pass


@dataclass
class TokenTracker:
    """Track token usage across agent loop execution."""

    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cache_read_tokens: int = 0
    total_cache_creation_tokens: int = 0

    def add_usage(self, usage: TokenUsage) -> None:
        """Add token usage from a response."""
        self.total_input_tokens += usage.input_tokens
        self.total_output_tokens += usage.output_tokens
        self.total_cache_read_tokens += usage.cache_read_tokens
        self.total_cache_creation_tokens += usage.cache_creation_tokens

        self._validate()

    def _validate(self) -> None:
        """Validate token counts are non-negative."""
        if self.total_input_tokens < 0:
            raise ValueError("Input tokens cannot be negative")
        if self.total_output_tokens < 0:
            raise ValueError("Output tokens cannot be negative")

    def get_total_tokens(self) -> int:
        """Get total tokens used."""
        return (
            self.total_input_tokens
            + self.total_output_tokens
            + self.total_cache_read_tokens
            + self.total_cache_creation_tokens
        )


async def agent_loop(
    messages: list[dict[str, Any]],
    config: AgentConfig,
    llm_client: LLMClient,
    tool_executor: ToolExecutor | None = None,
    cancellation_token: CancellationToken | None = None,
    short_term_memory: ShortTermMemory | None = None,
    long_term_memory: LongTermMemory | None = None,
    memory_bridge: MemoryBridge | None = None,
    concurrency_manager: ConcurrencyManager | None = None,
) -> AsyncIterator[AgentEvent]:
    """Execute the agent loop.

    This is the main agent execution loop that handles:
    - LLM communication
    - Tool execution
    - Memory management
    - Token tracking

    Args:
        messages: Initial messages to process.
        config: Agent configuration.
        llm_client: LLM client for communication.
        tool_executor: Optional tool executor for running tools.
        cancellation_token: Optional token for cancelling execution.
        short_term_memory: Optional short-term memory instance.
        long_term_memory: Optional long-term memory instance.
        memory_bridge: Optional memory bridge for transferring memories.
        concurrency_manager: Optional concurrency manager for limiting parallel operations.

    Yields:
        AgentEvent instances representing the execution progress.
    """
    token_tracker = TokenTracker()
    current_messages = list(messages)
    round_count = 0

    if concurrency_manager is None:
        concurrency_manager = ConcurrencyManager()

    if short_term_memory is None:
        short_term_memory = ShortTermMemory(max_tokens=config.max_tokens)
    if long_term_memory is None:
        long_term_memory = LongTermMemory()
    if memory_bridge is None:
        memory_bridge = MemoryBridge(short_term_memory, long_term_memory)

    while round_count < config.max_tool_rounds:
        if cancellation_token and cancellation_token.is_cancelled:
            yield AgentEvent(
                event_type=EventType.ERROR,
                content="Execution cancelled by user",
            )
            return

        if token_tracker.get_total_tokens() > config.token_budget:
            yield AgentEvent(
                event_type=EventType.ERROR,
                content=f"Token budget exceeded: {token_tracker.get_total_tokens()} > {config.token_budget}",
            )
            return
        try:
            if current_messages:
                last_message = current_messages[-1]
                if 'content' in last_message:
                    search_query = last_message['content']
                    relevant_memories = await long_term_memory.search_memory(search_query, limit=3)
                    if relevant_memories:
                        for memory in relevant_memories:
                            current_messages.append({
                                "role": "system",
                                "content": f"[Memory] {memory['content']}"
                            })
            response = await llm_client.chat(
                messages=current_messages,
                model=config.model,
                max_tokens=config.max_tokens,
                tools=config.tools if config.tools else None,
                system_prompt=config.system_prompt,
            )
            if response.token_usage:
                token_tracker.add_usage(response.token_usage)
            if token_tracker.get_total_tokens() > config.token_budget:
                yield AgentEvent(
                    event_type=EventType.ERROR,
                    content=f"Token budget exceeded: {token_tracker.get_total_tokens()} > {config.token_budget}",
                )
                return
            if response.content:
                yield AgentEvent(
                    event_type=EventType.TEXT,
                    content=response.content,
                    token_usage=response.token_usage,
                )
                short_term_memory.add_item({
                    "role": "assistant",
                    "content": response.content,
                    "timestamp": "current"
                })
            if not response.tool_calls or not tool_executor:
                break
            async def execute_single_tool(
                tool_call: ToolCall,
            ) -> tuple[ToolCall, str, dict[str, Any]]:
                async with concurrency_manager.limit():
                    result_content, result_metadata = await tool_executor.execute_tool(
                        tool_name=tool_call.tool_name,
                        tool_input=tool_call.tool_input,
                        call_id=tool_call.call_id,
                    )
                    return tool_call, result_content, result_metadata
            if len(response.tool_calls) > 1:
                tool_tasks = [
                    execute_single_tool(tool_call)
                    for tool_call in response.tool_calls
                ]
                tool_results = await asyncio.gather(*tool_tasks, return_exceptions=True)
                for result in tool_results:
                    if isinstance(result, BaseException):
                        yield AgentEvent(
                            event_type=EventType.ERROR,
                            content=f"Tool execution failed: {result}",
                        )
                        continue
                    tool_call, result_content, result_metadata = result
                    yield AgentEvent(
                        event_type=EventType.TOOL_USE,
                        content=tool_call.tool_name,
                        metadata={"tool_input": tool_call.tool_input, "call_id": tool_call.call_id},
                    )
                    yield AgentEvent(
                        event_type=EventType.TOOL_RESULT,
                        content=result_content,
                        metadata=result_metadata,
                    )
                    short_term_memory.add_item({
                        "role": "tool",
                        "content": f"Tool {tool_call.tool_name} result: {result_content}",
                        "metadata": result_metadata,
                        "timestamp": "current"
                    })
                    current_messages.append({
                        "role": "assistant",
                        "content": response.content,
                        "tool_calls": [{
                            "id": tool_call.call_id,
                            "type": "function",
                            "function": {
                                "name": tool_call.tool_name,
                                "arguments": str(tool_call.tool_input),
                            },
                        }],
                    })
                    current_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.call_id,
                        "content": result_content,
                    })
            else:
                for tool_call in response.tool_calls:
                    yield AgentEvent(
                        event_type=EventType.TOOL_USE,
                        content=tool_call.tool_name,
                        metadata={"tool_input": tool_call.tool_input, "call_id": tool_call.call_id},
                    )
                    async with concurrency_manager.limit():
                        result_content, result_metadata = await tool_executor.execute_tool(
                            tool_name=tool_call.tool_name,
                            tool_input=tool_call.tool_input,
                            call_id=tool_call.call_id,
                        )
                    yield AgentEvent(
                        event_type=EventType.TOOL_RESULT,
                        content=result_content,
                        metadata=result_metadata,
                    )
                    short_term_memory.add_item({
                        "role": "tool",
                        "content": f"Tool {tool_call.tool_name} result: {result_content}",
                        "metadata": result_metadata,
                        "timestamp": "current"
                    })
                    current_messages.append(
                        {
                            "role": "assistant",
                            "content": response.content,
                            "tool_calls": [
                                {
                                    "id": tool_call.call_id,
                                    "type": "function",
                                    "function": {
                                        "name": tool_call.tool_name,
                                        "arguments": str(tool_call.tool_input),
                                    },
                                }
                            ],
                        }
                    )
                    current_messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.call_id,
                            "content": result_content,
                        }
                    )
        except Exception as e:
            yield AgentEvent(
                event_type=EventType.ERROR,
                content=str(e),
            )
            return
        round_count += 1
    try:
        memory_stats = await memory_bridge.process_memory_cycle(
            importance_threshold=0.5,
            clear_short_term=False
        )
        yield AgentEvent(
            event_type=EventType.MEMORY_TRANSFER,
            content=f"Memory transfer completed: {memory_stats['transferred_count']} items transferred",
            metadata=memory_stats
        )
    except Exception as e:
        yield AgentEvent(
            event_type=EventType.ERROR,
            content=f"Memory transfer failed: {str(e)}",
        )
