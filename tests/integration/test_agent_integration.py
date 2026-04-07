import pytest
import sys
from unittest.mock import Mock, patch
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_startup(runner):
    """测试 CLI 启动"""
    # 模拟 textual 模块
    with patch.dict('sys.modules', {
        'textual': Mock(),
        'textual.app': Mock(),
        'textual.app.App': Mock(),
        'textual.app.ComposeResult': Mock(),
        'textual.containers': Mock(),
        'textual.widgets': Mock(),
        'textual.keys': Mock(),
        'textual.events': Mock(),
        'sherry_agent.cli.tui': Mock(),
        'sherry_agent.cli.widgets': Mock(),
        'sherry_agent.cli.widgets.TerminalOutput': Mock(),
        'sherry_agent.cli.widgets.UserInput': Mock(),
        'sherry_agent.cli.widgets.StatusBar': Mock(),
    }):
        from sherry_agent.cli.main import cli
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "SherryAgent" in result.output
        assert "--help" in result.output
        assert "run" in result.output
        assert "status" in result.output


def test_cli_status_command(runner):
    """测试 status 命令"""
    # 模拟 textual 模块
    with patch.dict('sys.modules', {
        'textual': Mock(),
        'textual.app': Mock(),
        'textual.app.App': Mock(),
        'textual.app.ComposeResult': Mock(),
        'textual.containers': Mock(),
        'textual.widgets': Mock(),
        'textual.keys': Mock(),
        'textual.events': Mock(),
        'sherry_agent.cli.tui': Mock(),
        'sherry_agent.cli.widgets': Mock(),
        'sherry_agent.cli.widgets.TerminalOutput': Mock(),
        'sherry_agent.cli.widgets.UserInput': Mock(),
        'sherry_agent.cli.widgets.StatusBar': Mock(),
    }):
        from sherry_agent.cli.main import cli
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "SherryAgent 状态:" in result.output
        assert "核心Agent Loop: 📝 规划中" in result.output
        assert "记忆系统: 📝 规划中" in result.output
        assert "自主运行: 📝 规划中" in result.output
        assert "多Agent编排: 📝 规划中" in result.output
        assert "插件生态: 📝 规划中" in result.output


def test_cli_version_command(runner):
    """测试版本命令"""
    # 模拟 textual 模块
    with patch.dict('sys.modules', {
        'textual': Mock(),
        'textual.app': Mock(),
        'textual.app.App': Mock(),
        'textual.app.ComposeResult': Mock(),
        'textual.containers': Mock(),
        'textual.widgets': Mock(),
        'textual.keys': Mock(),
        'textual.events': Mock(),
        'sherry_agent.cli.tui': Mock(),
        'sherry_agent.cli.widgets': Mock(),
        'sherry_agent.cli.widgets.TerminalOutput': Mock(),
        'sherry_agent.cli.widgets.UserInput': Mock(),
        'sherry_agent.cli.widgets.StatusBar': Mock(),
    }):
        from sherry_agent.cli.main import cli
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "sherry-agent, version" in result.output
