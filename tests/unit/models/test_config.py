import pytest
from sherry_agent.models import AgentConfig


class TestAgentConfig:
    def test_agent_config_defaults(self):
        config = AgentConfig()
        assert config.model == "claude-sonnet-4-20250514"
        assert config.max_tokens == 8192
        assert config.token_budget == 200_000
        assert config.max_tool_rounds == 20
        assert config.system_prompt == ""
        assert config.tools == []

    def test_agent_config_custom_values(self):
        tools = [{"name": "search", "description": "Search tool"}]
        config = AgentConfig(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            token_budget=100_000,
            max_tool_rounds=10,
            system_prompt="You are a helpful assistant",
            tools=tools,
        )
        assert config.model == "claude-3-opus-20240229"
        assert config.max_tokens == 4096
        assert config.token_budget == 100_000
        assert config.max_tool_rounds == 10
        assert config.system_prompt == "You are a helpful assistant"
        assert config.tools == tools

    def test_agent_config_tools_defaults_to_empty_list(self):
        config = AgentConfig()
        assert config.tools == []
        assert isinstance(config.tools, list)

    def test_agent_config_immutable_defaults(self):
        config1 = AgentConfig()
        config2 = AgentConfig()
        assert config1.tools is not config2.tools
        config1.tools.append({"name": "test"})
        assert config2.tools == []
