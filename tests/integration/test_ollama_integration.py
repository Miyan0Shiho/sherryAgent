
"""
Ollama 集成测试
"""

import pytest
import aiohttp

from sherry_agent.llm import OllamaClient
from sherry_agent.execution.agent_loop import agent_loop
from sherry_agent.models.config import AgentConfig
from sherry_agent.models.events import EventType


async def is_ollama_available():
    """检查 Ollama 服务是否可用"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                return response.status == 200
    except Exception:
        return False


@pytest.fixture(scope="module")
def ollama_available():
    """检查 Ollama 服务是否可用的 fixture"""
    import asyncio
    return asyncio.run(is_ollama_available())


@pytest.fixture
def ollama_client():
    """创建 Ollama 客户端 fixture"""
    return OllamaClient()


@pytest.fixture
def agent_config():
    """创建 Agent 配置 fixture"""
    return AgentConfig(
        model="qwen3:0.6b",
        max_tokens=500,
        system_prompt="你是一个有用的助手。"
    )


@pytest.mark.integration
@pytest.mark.ollama
@pytest.mark.asyncio
async def test_ollama_connection(ollama_available, ollama_client):
    """测试 Ollama 客户端能正常连接本地服务"""
    if not ollama_available:
        pytest.skip("Ollama 服务不可用")
    
    try:
        response = await ollama_client.chat(
            messages=[{"role": "user", "content": "你好"}],
            model="qwen3:0.6b",
            max_tokens=100
        )
        assert response is not None
        assert response.content is not None
        assert isinstance(response.content, str)
    except Exception as e:
        pytest.fail(f"连接 Ollama 服务失败: {str(e)}")


@pytest.mark.integration
@pytest.mark.ollama
@pytest.mark.asyncio
async def test_ollama_simple_chat(ollama_available, ollama_client):
    """测试与 qwen3:0.6b 模型的简单对话"""
    if not ollama_available:
        pytest.skip("Ollama 服务不可用")
    
    messages = [
        {"role": "user", "content": "请用一句话介绍自己"}
    ]
    
    response = await ollama_client.chat(
        messages=messages,
        model="qwen3:0.6b",
        max_tokens=200
    )
    
    assert response is not None
    assert response.content is not None
    assert len(response.content.strip()) > 0


@pytest.mark.integration
@pytest.mark.ollama
@pytest.mark.asyncio
async def test_ollama_multi_turn_chat(ollama_available, ollama_client):
    """测试与 qwen3:0.6b 模型的多轮对话"""
    if not ollama_available:
        pytest.skip("Ollama 服务不可用")
    
    messages = [
        {"role": "user", "content": "我的名字叫 Sherry"},
        {"role": "assistant", "content": "你好 Sherry！很高兴认识你。"},
        {"role": "user", "content": "我叫什么名字？"}
    ]
    
    response = await ollama_client.chat(
        messages=messages,
        model="qwen3:0.6b",
        max_tokens=200
    )
    
    assert response is not None
    assert response.content is not None
    assert "Sherry" in response.content or "sherry" in response.content


@pytest.mark.integration
@pytest.mark.ollama
@pytest.mark.asyncio
async def test_agent_loop_with_ollama(ollama_available, ollama_client, agent_config):
    """测试完整的 Agent Loop 与真实 Ollama 模型的集成"""
    if not ollama_available:
        pytest.skip("Ollama 服务不可用")
    
    messages = [
        {"role": "user", "content": "你好，请介绍一下自己，并告诉我你能做什么"}
    ]
    
    events = []
    async for event in agent_loop(
        messages=messages,
        config=agent_config,
        llm_client=ollama_client
    ):
        events.append(event)
    
    assert len(events) > 0
    assert events[0].event_type == EventType.TEXT
    assert len(events[0].content.strip()) > 0

