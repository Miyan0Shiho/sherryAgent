from typing import Any, Callable, Dict, List, Optional, TypeVar, cast
from functools import wraps


T = TypeVar('T', bound=Callable[..., Any])

# 定义工具属性的类型
tool_name: str
tool_description: str
tool_parameters: Dict[str, Any]
tool_permissions: Optional[List[str]]


def plugin(cls: Any) -> Any:
    """插件装饰器
    
    用于标记一个类为SherryAgent插件。
    
    Args:
        cls: 插件类
        
    Returns:
        装饰后的插件类
    """
    # 确保类实现了必要的属性
    required_attrs = ['name', 'version', 'description']
    for attr in required_attrs:
        if not hasattr(cls, attr):
            raise ValueError(f"Plugin class must have '{attr}' attribute")
    
    return cls


def tool(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    permissions: Optional[List[str]] = None
) -> Callable[[T], T]:
    """工具装饰器
    
    用于标记一个函数为SherryAgent工具。
    
    Args:
        name: 工具名称
        description: 工具描述
        parameters: 工具参数，遵循JSON Schema格式
        permissions: 工具所需的权限
        
    Returns:
        装饰器函数
    """
    def decorator(func: T) -> T:
        # 直接在函数对象上设置属性
        func.__tool_name__ = name  # type: ignore[attr-defined]
        func.__tool_description__ = description  # type: ignore[attr-defined]
        func.__tool_parameters__ = parameters  # type: ignore[attr-defined]
        func.__tool_permissions__ = permissions  # type: ignore[attr-defined]
        
        return func
    
    return decorator
