"""子Agent派生器"""

from typing import Optional, List

from .models import ForkConfig


class AgentContext:
    """Agent上下文"""

    def __init__(self, system_prompt_prefix="", system_prompt_suffix="", tools=None, permissions=None):
        """
        初始化Agent上下文

        Args:
            system_prompt_prefix: 系统提示前缀
            system_prompt_suffix: 系统提示后缀
            tools: 工具列表
            permissions: 权限列表
        """
        self.system_prompt_prefix = system_prompt_prefix
        self.system_prompt_suffix = system_prompt_suffix
        self.tools = tools or []
        self.permissions = permissions or []


class SubAgent:
    """子Agent"""

    def __init__(self, system_prompt: str, tools: List, permissions: List[str]):
        """
        初始化子Agent

        Args:
            system_prompt: 系统提示
            tools: 工具列表
            permissions: 权限列表
        """
        self.system_prompt = system_prompt
        self.tools = tools
        self.permissions = permissions


class AgentForker:
    """子Agent派生器"""

    async def fork(
        self, parent_context: AgentContext, config: ForkConfig
    ) -> SubAgent:
        """
        从父Agent上下文派生子Agent。

        继承系统提示前缀以复用prompt cache，
        配置独立的工具池和权限。

        Args:
            parent_context: 父Agent上下文
            config: Fork配置

        Returns:
            子Agent实例
        """
        # 继承系统提示前缀
        system_prompt = ""
        if hasattr(parent_context, 'system_prompt_prefix'):
            system_prompt = parent_context.system_prompt_prefix
        
        if config.inherit_system_prompt:
            if hasattr(parent_context, 'system_prompt_suffix'):
                system_prompt += parent_context.system_prompt_suffix
        
        # 配置独立工具池
        tools = []
        if parent_context.tools:
            if config.inherit_tools is None:
                # 继承所有工具
                tools = parent_context.tools.copy()
            else:
                # 继承指定工具
                for tool in parent_context.tools:
                    if isinstance(tool, str) and tool in config.inherit_tools:
                        tools.append(tool)
                    elif hasattr(tool, 'name') and tool.name in config.inherit_tools:
                        tools.append(tool)
                    elif hasattr(tool, '__name__') and tool.__name__ in config.inherit_tools:
                        tools.append(tool)
        
        # 添加额外工具
        tools.extend(config.extra_tools)

        # 合并权限
        permissions = []
        if hasattr(parent_context, 'permissions'):
            permissions = parent_context.permissions.copy()
        permissions.extend(config.extra_permissions)

        return SubAgent(
            system_prompt=system_prompt,
            tools=tools,
            permissions=permissions
        )


__all__ = ["AgentForker", "SubAgent"]