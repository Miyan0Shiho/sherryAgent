from __future__ import annotations

import pluggy
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from sherry_agent.infrastructure.tools.base import BaseTool, ToolDefinition

# 创建 hookspec 装饰器
hookspec = pluggy.HookspecMarker("sherry_agent")


@runtime_checkable
class Plugin(Protocol):
    """插件协议"""
    @property
    def name(self) -> str:
        """插件名称"""
        ...

    @property
    def version(self) -> str:
        """插件版本"""
        ...

    @property
    def description(self) -> str:
        """插件描述"""
        ...
    
    @property
    def dependencies(self) -> List[str]:
        """插件依赖"""
        ...


class PluginHooks:
    """插件钩子规范"""

    @staticmethod
    @hookspec
    def plugin_loaded(plugin: Plugin) -> None:
        """插件加载时触发"""
        pass

    @staticmethod
    @hookspec
    def plugin_unloaded(plugin: Plugin) -> None:
        """插件卸载时触发"""
        pass

    @staticmethod
    @hookspec
    def get_tools() -> List[BaseTool | ToolDefinition]:
        """获取插件提供的工具"""
        return []

    @staticmethod
    @hookspec
    def agent_started(agent_id: str, config: Dict[str, Any]) -> None:
        """Agent 启动时触发"""
        pass

    @staticmethod
    @hookspec
    def agent_stopped(agent_id: str, status: str) -> None:
        """Agent 停止时触发"""
        pass
    
    @staticmethod
    @hookspec
    def plugin_enabled(plugin: Plugin) -> None:
        """插件启用时触发"""
        pass
    
    @staticmethod
    @hookspec
    def plugin_disabled(plugin: Plugin) -> None:
        """插件禁用时触发"""
        pass


# 创建 pluggy 插件管理器
plugin_hooks = pluggy.PluginManager("sherry_agent")

# 注册钩子规范
plugin_hooks.add_hookspecs(PluginHooks)
