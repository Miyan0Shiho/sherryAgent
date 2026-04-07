from typing import List, Dict, Any, Optional
from sherry_agent.plugins.hooks import Plugin


class BasePlugin(Plugin):
    """插件基类
    
    所有SherryAgent插件都应该继承此类。
    """
    
    @property
    def name(self) -> str:
        """插件名称
        
        必须返回插件的唯一名称。
        """
        raise NotImplementedError
    
    @property
    def version(self) -> str:
        """插件版本
        
        必须返回插件的版本号，遵循语义化版本规范。
        """
        raise NotImplementedError
    
    @property
    def description(self) -> str:
        """插件描述
        
        必须返回插件的详细描述。
        """
        raise NotImplementedError
    
    @property
    def dependencies(self) -> List[str]:
        """插件依赖
        
        返回插件依赖的其他插件列表。
        """
        return []
    
    def get_tools(self) -> List[Any]:
        """获取插件提供的工具
        
        返回插件提供的工具列表，工具可以是BaseTool实例或ToolDefinition对象。
        """
        return []
    
    def agent_started(self, agent_id: str, config: Dict[str, Any]) -> None:
        """Agent启动时触发
        
        Args:
            agent_id: Agent的唯一标识符
            config: Agent的配置信息
        """
        pass
    
    def agent_stopped(self, agent_id: str, status: str) -> None:
        """Agent停止时触发
        
        Args:
            agent_id: Agent的唯一标识符
            status: Agent的停止状态
        """
        pass
    
    def plugin_enabled(self, plugin: Plugin) -> None:
        """插件启用时触发
        
        Args:
            plugin: 被启用的插件
        """
        pass
    
    def plugin_disabled(self, plugin: Plugin) -> None:
        """插件禁用时触发
        
        Args:
            plugin: 被禁用的插件
        """
        pass
