import pytest
import sys
from unittest.mock import Mock, patch
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_version(runner):
    """测试 CLI 版本命令"""
    # 保存原始模块
    original_modules = sys.modules.copy()
    
    try:
        # 模拟 textual 模块
        sys.modules['textual'] = Mock()
        sys.modules['textual.app'] = Mock()
        sys.modules['textual.app'].App = Mock()
        sys.modules['textual.app'].ComposeResult = Mock()
        
        # 模拟 TUI 模块
        sys.modules['sherry_agent.cli.tui'] = Mock()
        sys.modules['sherry_agent.cli.tui'].SherryAgentTUI = Mock()
        
        # 导入并测试
        from sherry_agent.cli.main import cli
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "sherry-agent, version" in result.output
    finally:
        # 恢复原始模块
        sys.modules.update(original_modules)


def test_cli_status_command(runner):
    """测试 status 命令"""
    # 保存原始模块
    original_modules = sys.modules.copy()
    
    try:
        # 模拟 textual 模块
        sys.modules['textual'] = Mock()
        sys.modules['textual.app'] = Mock()
        sys.modules['textual.app'].App = Mock()
        sys.modules['textual.app'].ComposeResult = Mock()
        
        # 模拟 TUI 模块
        sys.modules['sherry_agent.cli.tui'] = Mock()
        sys.modules['sherry_agent.cli.tui'].SherryAgentTUI = Mock()
        
        # 导入并测试
        from sherry_agent.cli.main import cli
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "SherryAgent 状态:" in result.output
        assert "核心Agent Loop: ✅ 已完成" in result.output
        assert "记忆系统: ✅ 已完成" in result.output
        assert "自主运行: 🔄 开发中" in result.output
        assert "多Agent编排: 📝 规划中" in result.output
        assert "插件生态: ✅ 已完成" in result.output
    finally:
        # 恢复原始模块
        sys.modules.update(original_modules)
