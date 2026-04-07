import pytest
import asyncio
from typing import Any

from src.sherry_agent.execution.agent_loop import ToolExecutor, TokenTracker, agent_loop
from src.sherry_agent.llm.client import LLMResponse, MockLLMClient
from src.sherry_agent.models.config import AgentConfig
from src.sherry_agent.models.events import AgentEvent, CancellationToken, EventType, TokenUsage, ToolCall


class MockToolExecutor(ToolExecutor):
    async def execute_tool(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        call_id: str,
    ) -> tuple[str, dict[str, Any]]:
        if tool_name == "test_tool":
            return f"Executed {tool_name} with {tool_input}", {"call_id": call_id}
        elif tool_name == "calculate":
            a = tool_input.get("a", 0)
            b = tool_input.get("b", 0)
            op = tool_input.get("op", "+")
            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            elif op == "/":
                result = a / b if b != 0 else "Error: Division by zero"
            else:
                result = f"Unknown operation: {op}"
            return str(result), {"call_id": call_id, "result": result}
        elif tool_name == "search":
            query = tool_input.get("query", "")
            return f"Search results for: {query}", {"call_id": call_id}
        return "Unknown tool", {"call_id": call_id}


class MockLLMClientWithTools(MockLLMClient):
    def __init__(
        self,
        responses: list[str] | None = None,
        tool_call_sequences: list[list[ToolCall]] | None = None,
    ) -> None:
        super().__init__(responses)
        self.tool_call_sequences = tool_call_sequences or []

    async def chat(
        self,
        messages: list[dict[str, Any]],
        model: str,
        max_tokens: int,
        tools: list[dict[str, Any]] | None = None,
        system_prompt: str = "",
    ) -> LLMResponse:
        content = self.responses[self._response_index % len(self.responses)]
        tool_calls_for_response = []
        if self._response_index < len(self.tool_call_sequences):
            tool_calls_for_response = self.tool_call_sequences[self._response_index]
        self._response_index += 1
        return LLMResponse(
            content=content,
            tool_calls=tool_calls_for_response,
            token_usage=TokenUsage(input_tokens=100, output_tokens=50),
        )


def test_token_tracker():
    tracker = TokenTracker()
    
    usage1 = TokenUsage(input_tokens=100, output_tokens=50)
    tracker.add_usage(usage1)
    assert tracker.get_total_tokens() == 150
    
    usage2 = TokenUsage(input_tokens=200, output_tokens=100, cache_read_tokens=50)
    tracker.add_usage(usage2)
    assert tracker.get_total_tokens() == 500


@pytest.mark.asyncio
async def test_agent_loop_basic():
    config = AgentConfig()
    llm_client = MockLLMClient(responses=["Hello, world!"])
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "Hello"}],
        config=config,
        llm_client=llm_client,
    ):
        events.append(event)
    
    assert len(events) == 2  # 包含记忆转移事件
    assert events[0].event_type == EventType.TEXT
    assert events[0].content == "Hello, world!"
    assert events[0].token_usage is not None
    assert events[0].token_usage.input_tokens == 100
    assert events[0].token_usage.output_tokens == 50


@pytest.mark.asyncio
async def test_agent_loop_complete_tool_call_flow():
    config = AgentConfig(tools=[
        {"name": "calculate"},
        {"name": "search"}
    ])
    
    tool_call = ToolCall(
        tool_name="calculate",
        tool_input={"a": 5, "b": 3, "op": "+"},
        call_id="calc_001"
    )
    
    llm_client = MockLLMClientWithTools(
        responses=["Calculating 5 + 3...", "The result is 8!"],
        tool_call_sequences=[[tool_call], []]
    )
    
    tool_executor = MockToolExecutor()
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "What's 5 + 3?"}],
        config=config,
        llm_client=llm_client,
        tool_executor=tool_executor,
    ):
        events.append(event)
    
    assert len(events) == 5  # 包含记忆转移事件
    
    assert events[0].event_type == EventType.TEXT
    assert "Calculating" in events[0].content
    
    assert events[1].event_type == EventType.TOOL_USE
    assert events[1].content == "calculate"
    assert events[1].metadata["tool_input"] == {"a": 5, "b": 3, "op": "+"}
    assert events[1].metadata["call_id"] == "calc_001"
    
    assert events[2].event_type == EventType.TOOL_RESULT
    assert events[2].content == "8"
    assert events[2].metadata["call_id"] == "calc_001"
    assert events[2].metadata["result"] == 8
    
    assert events[3].event_type == EventType.TEXT
    assert events[3].content == "The result is 8!"


@pytest.mark.asyncio
async def test_agent_loop_multi_turn_conversation():
    config = AgentConfig(tools=[{"name": "search"}, {"name": "calculate"}])
    
    tool_call1 = ToolCall(
        tool_name="search",
        tool_input={"query": "Paris population"},
        call_id="search_001"
    )
    tool_call2 = ToolCall(
        tool_name="calculate",
        tool_input={"a": 2100000, "b": 1000000, "op": "+"},
        call_id="calc_002"
    )
    
    llm_client = MockLLMClientWithTools(
        responses=[
            "Let me search for Paris population...",
            "Paris has about 2.1 million people. Let's calculate...",
            "Total is 3.1 million!"
        ],
        tool_call_sequences=[[tool_call1], [tool_call2], []]
    )
    
    tool_executor = MockToolExecutor()
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "What's Paris population plus 1 million?"}],
        config=config,
        llm_client=llm_client,
        tool_executor=tool_executor,
    ):
        events.append(event)
    
    assert len(events) == 8  # 包含记忆转移事件
    
    assert events[0].event_type == EventType.TEXT
    assert events[1].event_type == EventType.TOOL_USE
    assert events[1].content == "search"
    assert events[2].event_type == EventType.TOOL_RESULT
    assert events[3].event_type == EventType.TEXT
    assert events[4].event_type == EventType.TOOL_USE
    assert events[4].content == "calculate"
    assert events[5].event_type == EventType.TOOL_RESULT
    assert events[6].event_type == EventType.TEXT


@pytest.mark.asyncio
async def test_agent_loop_token_budget_control():
    config = AgentConfig(token_budget=140)
    llm_client = MockLLMClient(responses=["Response 1", "Response 2", "Response 3"])
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "Hello"}],
        config=config,
        llm_client=llm_client,
    ):
        events.append(event)
    
    assert len(events) == 1  # 错误情况下不会执行记忆转移
    assert events[0].event_type == EventType.ERROR
    assert "Token budget exceeded" in events[0].content


@pytest.mark.asyncio
async def test_agent_loop_token_budget_control_multiple_rounds():
    config = AgentConfig(token_budget=300, tools=[{"name": "test_tool"}])
    
    tool_call = ToolCall(
        tool_name="test_tool",
        tool_input={"param": "value"},
        call_id="call_123"
    )
    
    llm_client = MockLLMClientWithTools(
        responses=["Round 1", "Round 2", "Round 3"],
        tool_call_sequences=[[tool_call], [tool_call]]
    )
    
    tool_executor = MockToolExecutor()
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "Hello"}],
        config=config,
        llm_client=llm_client,
        tool_executor=tool_executor,
    ):
        events.append(event)
    
    assert len(events) >= 1
    has_error = any(event.event_type == EventType.ERROR and "Token budget exceeded" in event.content for event in events)
    assert has_error


@pytest.mark.asyncio
async def test_agent_loop_cancellation_at_start():
    config = AgentConfig()
    llm_client = MockLLMClient(responses=["Hello, world!"])
    cancellation_token = CancellationToken()
    cancellation_token.cancel()
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "Hello"}],
        config=config,
        llm_client=llm_client,
        cancellation_token=cancellation_token,
    ):
        events.append(event)
    
    assert len(events) == 1  # 错误情况下不会执行记忆转移
    assert events[0].event_type == EventType.ERROR
    assert "Execution cancelled by user" in events[0].content


@pytest.mark.asyncio
async def test_agent_loop_cancellation_during_execution():
    config = AgentConfig(tools=[{"name": "test_tool"}])
    tool_call = ToolCall(
        tool_name="test_tool",
        tool_input={"param": "value"},
        call_id="call_123"
    )
    
    class SlowMockToolExecutor(ToolExecutor):
        def __init__(self, cancellation_token: CancellationToken) -> None:
            self.cancellation_token = cancellation_token
        
        async def execute_tool(
            self,
            tool_name: str,
            tool_input: dict[str, Any],
            call_id: str,
        ) -> tuple[str, dict[str, Any]]:
            await asyncio.sleep(0.01)
            self.cancellation_token.cancel()
            return "Result", {"call_id": call_id}
    
    cancellation_token = CancellationToken()
    llm_client = MockLLMClientWithTools(
        responses=["Using tool...", "Done!"],
        tool_call_sequences=[[tool_call]]
    )
    tool_executor = SlowMockToolExecutor(cancellation_token)
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "Test"}],
        config=config,
        llm_client=llm_client,
        tool_executor=tool_executor,
        cancellation_token=cancellation_token,
    ):
        events.append(event)
    
    assert len(events) >= 1
    assert any(event.event_type == EventType.ERROR and "cancelled" in event.content for event in events)


@pytest.mark.asyncio
async def test_agent_loop_no_tools_provided():
    config = AgentConfig()
    tool_call = ToolCall(
        tool_name="test_tool",
        tool_input={"param": "value"},
        call_id="call_123"
    )
    
    llm_client = MockLLMClientWithTools(
        responses=["I need to use a tool", "Done without tools"],
        tool_call_sequences=[[tool_call]]
    )
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "Hello"}],
        config=config,
        llm_client=llm_client,
        tool_executor=None,
    ):
        events.append(event)
    
    assert len(events) == 2  # 包含记忆转移事件
    assert events[0].event_type == EventType.TEXT
    assert events[0].content == "I need to use a tool"


@pytest.mark.asyncio
async def test_agent_loop_max_tool_rounds():
    config = AgentConfig(
        tools=[{"name": "test_tool"}],
        max_tool_rounds=2
    )
    
    tool_call = ToolCall(
        tool_name="test_tool",
        tool_input={"param": "value"},
        call_id="call_123"
    )
    
    llm_client = MockLLMClientWithTools(
        responses=["Round 1", "Round 2", "Round 3", "Done!"],
        tool_call_sequences=[[tool_call], [tool_call], [tool_call]]
    )
    
    tool_executor = MockToolExecutor()
    
    events = []
    async for event in agent_loop(
        messages=[{"role": "user", "content": "Hello"}],
        config=config,
        llm_client=llm_client,
        tool_executor=tool_executor,
    ):
        events.append(event)
    
    tool_use_events = [e for e in events if e.event_type == EventType.TOOL_USE]
    assert len(tool_use_events) == 2

