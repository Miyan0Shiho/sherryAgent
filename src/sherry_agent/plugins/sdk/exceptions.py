class PluginError(Exception):
    """插件错误基类"""
    pass


class ToolError(Exception):
    """工具错误基类"""
    pass


class PluginLoadError(PluginError):
    """插件加载错误"""
    pass


class PluginValidationError(PluginError):
    """插件验证错误"""
    pass


class ToolExecutionError(ToolError):
    """工具执行错误"""
    pass
