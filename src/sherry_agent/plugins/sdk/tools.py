from typing import Dict, Any, Optional, Callable, List, TypeVar, Generic
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class ToolDefinition:
    """工具定义
    
    用于定义插件提供的工具。
    """
    name: str
    """工具名称"""
    description: str
    """工具描述"""
    parameters: Dict[str, Any]
    """工具参数，遵循JSON Schema格式"""
    permissions: Optional[List[str]] = None
    """工具所需的权限"""
    func: Optional[Callable[..., Any]] = None
    """工具执行函数"""


class BaseTool:
    """工具基类
    
    所有SherryAgent工具都应该继承此类。
    """
    
    @property
    def name(self) -> str:
        """工具名称
        
        必须返回工具的唯一名称。
        """
        raise NotImplementedError
    
    @property
    def description(self) -> str:
        """工具描述
        
        必须返回工具的详细描述。
        """
        raise NotImplementedError
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """工具参数
        
        必须返回工具的参数定义，遵循JSON Schema格式。
        """
        raise NotImplementedError
    
    @property
    def permissions(self) -> Optional[List[str]]:
        """工具权限
        
        返回工具所需的权限列表。
        """
        return None
    
    async def execute(self, **kwargs: Any) -> Any:
        """执行工具
        
        Args:
            **kwargs: 工具执行参数
            
        Returns:
            工具执行结果
        """
        raise NotImplementedError
