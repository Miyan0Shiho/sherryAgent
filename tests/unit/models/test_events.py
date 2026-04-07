import pytest
from sherry_agent.models import (
    EventType,
    AgentEvent,
    TokenUsage,
    ToolCall,
    CancellationToken,
)


class TestEventType:
    def test_event_type_values(self):
        assert EventType.TEXT.value == "text"
        assert EventType.TOOL_USE.value == "tool_use"
        assert EventType.TOOL_RESULT.value == "tool_result"
        assert EventType.ERROR.value == "error"
        assert EventType.THINKING.value == "thinking"

    def test_event_type_members(self):
        assert len(EventType) == 6
        assert EventType.TEXT in EventType
        assert EventType.TOOL_USE in EventType
        assert EventType.MEMORY_TRANSFER in EventType


class TestTokenUsage:
    def test_token_usage_defaults(self):
        usage = TokenUsage()
        assert usage.input_tokens == 0
        assert usage.output_tokens == 0
        assert usage.cache_read_tokens == 0
        assert usage.cache_creation_tokens == 0

    def test_token_usage_custom_values(self):
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=200,
            cache_read_tokens=50,
            cache_creation_tokens=75,
        )
        assert usage.input_tokens == 100
        assert usage.output_tokens == 200
        assert usage.cache_read_tokens == 50
        assert usage.cache_creation_tokens == 75


class TestToolCall:
    def test_tool_call_creation(self):
        tool_call = ToolCall(
            tool_name="search",
            tool_input={"query": "test"},
            call_id="call-123",
        )
        assert tool_call.tool_name == "search"
        assert tool_call.tool_input == {"query": "test"}
        assert tool_call.call_id == "call-123"


class TestAgentEvent:
    def test_agent_event_minimal(self):
        event = AgentEvent(
            event_type=EventType.TEXT,
            content="Hello world",
        )
        assert event.event_type == EventType.TEXT
        assert event.content == "Hello world"
        assert event.metadata == {}
        assert event.token_usage is None

    def test_agent_event_full(self):
        usage = TokenUsage(input_tokens=100, output_tokens=50)
        event = AgentEvent(
            event_type=EventType.TOOL_USE,
            content="Using tool",
            metadata={"tool": "search"},
            token_usage=usage,
        )
        assert event.event_type == EventType.TOOL_USE
        assert event.content == "Using tool"
        assert event.metadata == {"tool": "search"}
        assert event.token_usage == usage


class TestCancellationToken:
    def test_cancellation_token_initial_state(self):
        token = CancellationToken()
        assert token.is_cancelled is False

    def test_cancellation_token_cancel(self):
        token = CancellationToken()
        token.cancel()
        assert token.is_cancelled is True

    def test_cancellation_token_multiple_cancel(self):
        token = CancellationToken()
        token.cancel()
        token.cancel()
        assert token.is_cancelled is True
