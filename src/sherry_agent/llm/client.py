
import importlib.util
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

import aiohttp

from ..models.events import AgentEvent, EventType, TokenUsage, ToolCall

_retry_path = Path(__file__).parent.parent / "infrastructure" / "retry.py"
_spec = importlib.util.spec_from_file_location("retry", _retry_path)
_retry_module = importlib.util.module_from_spec(_spec)
sys.modules["retry"] = _retry_module
_spec.loader.exec_module(_retry_module)
with_retry = _retry_module.with_retry
check_http_status = _retry_module.check_http_status

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

OLLAMA_AVAILABLE = True  # Ollama 通过 HTTP API 访问，不需要额外依赖


@dataclass
class LLMResponse:
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    token_usage: TokenUsage | None = None


class LLMClient(ABC):
    @abstractmethod
    async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
        pass

    @abstractmethod
    async def chat_stream(self, messages, model, max_tokens, tools=None, system_prompt=""):
        pass


if ANTHROPIC_AVAILABLE:
    class AnthropicClient(LLMClient):
        def __init__(self, api_key):
            self.client = anthropic.AsyncAnthropic(api_key=api_key)

        async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    anthropic_messages.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    anthropic_messages.append({"role": "assistant", "content": msg["content"]})

            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": anthropic_messages
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            if tools:
                kwargs["tools"] = tools

            response = await self.client.messages.create(**kwargs)

            content_text = ""
            tool_calls = []

            for block in response.content:
                if block.type == "text":
                    content_text += block.text
                elif block.type == "tool_use":
                    tool_calls.append(
                        ToolCall(
                            tool_name=block.name,
                            tool_input=block.input,
                            call_id=block.id
                        )
                    )

            token_usage = None
            if response.usage:
                token_usage = TokenUsage(
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens
                )

            return LLMResponse(
                content=content_text,
                tool_calls=tool_calls,
                token_usage=token_usage
            )

        async def chat_stream(self, messages, model, max_tokens, tools=None, system_prompt=""):
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    anthropic_messages.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    anthropic_messages.append({"role": "assistant", "content": msg["content"]})

            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": anthropic_messages
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            if tools:
                kwargs["tools"] = tools

            token_usage = None

            async with self.client.messages.stream(**kwargs) as stream:
                async for event in stream:
                    if event.type == "content_block_delta":
                        if event.delta.type == "text_delta":
                            yield AgentEvent(
                                event_type=EventType.TEXT,
                                content=event.delta.text
                            )
                    elif event.type == "message_delta":
                        if event.usage:
                            token_usage = TokenUsage(
                                input_tokens=event.usage.input_tokens or 0,
                                output_tokens=event.usage.output_tokens or 0
                            )

            if token_usage:
                yield AgentEvent(
                    event_type=EventType.TEXT,
                    content="",
                    token_usage=token_usage
                )
else:
    class AnthropicClient(LLMClient):
        def __init__(self, api_key):
            self.api_key = api_key

        async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
            return LLMResponse(
                content="Anthropic SDK 未安装，请安装: uv pip install anthropic"
            )

        async def chat_stream(self, messages, model, max_tokens, tools=None, system_prompt=""):
            yield AgentEvent(
                event_type=EventType.TEXT,
                content="Anthropic SDK 未安装，请安装: uv pip install anthropic"
            )


if OPENAI_AVAILABLE:
    class OpenAIClient(LLMClient):
        def __init__(self, api_key):
            self.client = openai.AsyncOpenAI(api_key=api_key)

        async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
            openai_messages = []
            if system_prompt:
                openai_messages.append({"role": "system", "content": system_prompt})
            openai_messages.extend(messages)

            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": openai_messages
            }
            if tools:
                kwargs["tools"] = tools

            response = await self.client.chat.completions.create(**kwargs)

            content_text = ""
            tool_calls = []

            choice = response.choices[0]
            if choice.message.content:
                content_text = choice.message.content

            if choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    tool_calls.append(
                        ToolCall(
                            tool_name=tool_call.function.name,
                            tool_input=tool_call.function.arguments,
                            call_id=tool_call.id
                        )
                    )

            token_usage = None
            if response.usage:
                token_usage = TokenUsage(
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens
                )

            return LLMResponse(
                content=content_text,
                tool_calls=tool_calls,
                token_usage=token_usage
            )

        async def chat_stream(self, messages, model, max_tokens, tools=None, system_prompt=""):
            openai_messages = []
            if system_prompt:
                openai_messages.append({"role": "system", "content": system_prompt})
            openai_messages.extend(messages)

            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": openai_messages,
                "stream": True,
                "stream_options": {"include_usage": True}
            }
            if tools:
                kwargs["tools"] = tools

            stream = await self.client.chat.completions.create(**kwargs)

            token_usage = None

            async for chunk in stream:
                if chunk.usage:
                    token_usage = TokenUsage(
                        input_tokens=chunk.usage.prompt_tokens or 0,
                        output_tokens=chunk.usage.completion_tokens or 0
                    )

                if chunk.choices and chunk.choices[0].delta.content:
                    yield AgentEvent(
                        event_type=EventType.TEXT,
                        content=chunk.choices[0].delta.content
                    )

            if token_usage:
                yield AgentEvent(
                    event_type=EventType.TEXT,
                    content="",
                    token_usage=token_usage
                )
else:
    class OpenAIClient(LLMClient):
        def __init__(self, api_key):
            self.api_key = api_key

        async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
            return LLMResponse(
                content="OpenAI SDK 未安装，请安装: uv pip install openai"
            )

        async def chat_stream(self, messages, model, max_tokens, tools=None, system_prompt=""):
            yield AgentEvent(
                event_type=EventType.TEXT,
                content="OpenAI SDK 未安装，请安装: uv pip install openai"
            )


class MockLLMClient(LLMClient):
    def __init__(self, responses=None):
        self.responses = responses or ["Hello! I'm a mock LLM client."]
        self._response_index = 0

    async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
        content = self.responses[self._response_index % len(self.responses)]
        self._response_index += 1
        return LLMResponse(
            content=content,
            token_usage=TokenUsage(input_tokens=100, output_tokens=50)
        )

    async def chat_stream(self, messages, model, max_tokens, tools=None, system_prompt=""):
        content = self.responses[self._response_index % len(self.responses)]
        self._response_index += 1

        import asyncio
        for char in content:
            await asyncio.sleep(0.01)
            yield AgentEvent(
                event_type=EventType.TEXT,
                content=char,
                token_usage=TokenUsage(input_tokens=100, output_tokens=1)
            )


class OllamaClient(LLMClient):
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(connect=5, sock_read=30)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    @with_retry(max_retries=3, base_delay=1.0, max_delay=30.0)
    async def chat(self, messages, model, max_tokens, tools=None, system_prompt=""):
        ollama_messages = []
        if system_prompt:
            ollama_messages.append({"role": "system", "content": system_prompt})
        ollama_messages.extend(messages)

        request_body = {
            "model": model,
            "messages": ollama_messages,
            "stream": False
        }
        if max_tokens:
            request_body["options"] = {"max_tokens": max_tokens}
        if tools:
            request_body["tools"] = tools

        session = await self._get_session()
        async with session.post(
            f"{self.base_url}/api/chat",
            json=request_body
        ) as response:
            check_http_status(response.status, await response.text())

            result = await response.json()
            content = result.get("message", {}).get("content", "")

            tool_calls = []
            if result.get("tool_calls"):
                for tool_call in result["tool_calls"]:
                    if tool_call.get("type") == "function":
                        function = tool_call.get("function", {})
                        tool_calls.append(
                            ToolCall(
                                tool_name=function.get("name"),
                                tool_input=function.get("arguments"),
                                call_id=tool_call.get("id")
                            )
                        )
            elif result.get("message", {}).get("tool_calls"):
                for tool_call in result["message"]["tool_calls"]:
                    if tool_call.get("function"):
                        function = tool_call.get("function", {})
                        tool_calls.append(
                            ToolCall(
                                tool_name=function.get("name"),
                                tool_input=function.get("arguments"),
                                call_id=tool_call.get("id")
                            )
                        )

            token_usage = TokenUsage(
                input_tokens=result.get("prompt_eval_count", 0),
                output_tokens=result.get("eval_count", 0),
                cache_read_tokens=0,
                cache_creation_tokens=0
            )

            return LLMResponse(
                content=content,
                tool_calls=tool_calls,
                token_usage=token_usage
            )

    @with_retry(max_retries=3, base_delay=1.0, max_delay=30.0)
    async def chat_stream(self, messages, model, max_tokens, tools=None, system_prompt=""):
        ollama_messages = []
        if system_prompt:
            ollama_messages.append({"role": "system", "content": system_prompt})
        ollama_messages.extend(messages)

        request_body = {
            "model": model,
            "messages": ollama_messages,
            "stream": True
        }
        if max_tokens:
            request_body["options"] = {"max_tokens": max_tokens}
        if tools:
            request_body["tools"] = tools

        session = await self._get_session()
        async with session.post(
            f"{self.base_url}/api/chat",
            json=request_body
        ) as response:
            check_http_status(response.status, await response.text())

            token_usage = None
            async for chunk in response.content:
                if not chunk:
                    continue

                try:
                    import json
                    line = chunk.decode('utf-8').strip()
                    if line.startswith('data: '):
                        line = line[6:]
                    if line == '[DONE]':
                        break

                    data = json.loads(line)

                    if 'message' in data and 'content' in data['message']:
                        content = data['message']['content']
                        if content:
                            yield AgentEvent(
                                event_type=EventType.TEXT,
                                content=content
                            )

                    if 'tool_calls' in data:
                        for tool_call in data['tool_calls']:
                            if tool_call.get('type') == 'function':
                                function = tool_call.get('function', {})
                                yield AgentEvent(
                                    event_type=EventType.TOOL_USE,
                                    content=function.get('name'),
                                    metadata={
                                        'tool_input': function.get('arguments'),
                                        'call_id': tool_call.get('id')
                                    }
                                )

                    if 'prompt_eval_count' in data and 'eval_count' in data:
                        token_usage = TokenUsage(
                            input_tokens=data.get('prompt_eval_count', 0),
                            output_tokens=data.get('eval_count', 0),
                            cache_read_tokens=0,
                            cache_creation_tokens=0
                        )
                except Exception as e:
                    yield AgentEvent(
                        event_type=EventType.TEXT,
                        content=f"解析 Ollama 响应时出错: {str(e)}"
                    )
                    break

            if token_usage:
                yield AgentEvent(
                    event_type=EventType.TEXT,
                    content="",
                    token_usage=token_usage
                )
