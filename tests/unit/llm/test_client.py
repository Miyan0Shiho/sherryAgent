import pytest
import asyncio

from src.sherry_agent.llm.client import LLMResponse, MockLLMClient
from src.sherry_agent.models.events import AgentEvent, EventType, TokenUsage


@pytest.mark.asyncio
async def test_mock_llm_client_chat():
    client = MockLLMClient(responses=["Test response 1", "Test response 2"])
    
    response1 = await client.chat(
        messages=[{"role": "user", "content": "Hello"}],
        model="test-model",
        max_tokens=100,
    )
    
    assert isinstance(response1, LLMResponse)
    assert response1.content == "Test response 1"
    assert response1.token_usage == TokenUsage(input_tokens=100, output_tokens=50)
    
    response2 = await client.chat(
        messages=[{"role": "user", "content": "Hello again"}],
        model="test-model",
        max_tokens=100,
    )
    
    assert response2.content == "Test response 2"


@pytest.mark.asyncio
async def test_mock_llm_client_chat_stream():
    client = MockLLMClient(responses=["Hello"])
    
    events = []
    async for event in client.chat_stream(
        messages=[{"role": "user", "content": "Hello"}],
        model="test-model",
        max_tokens=100,
    ):
        events.append(event)
    
    assert len(events) == 5
    assert all(isinstance(event, AgentEvent) for event in events)
    assert all(event.event_type == EventType.TEXT for event in events)
    
    full_content = "".join(event.content for event in events)
    assert full_content == "Hello"


@pytest.mark.asyncio
async def test_mock_llm_client_default_response():
    client = MockLLMClient()
    
    response = await client.chat(
        messages=[{"role": "user", "content": "Hello"}],
        model="test-model",
        max_tokens=100,
    )
    
    assert response.content == "Hello! I'm a mock LLM client."

