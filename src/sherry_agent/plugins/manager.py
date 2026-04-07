from __future__ import annotations

from typing import Dict, List, Optional, Any, TYPE_CHECKING

from sherry_agent.config.settings import settings
from sherry_agent.infrastructure.tools.base import BaseTool, ToolDefinition, get_tool, _TOOL_REGISTRY

from .hooks import Plugin, plugin_hooks
from .loader import PluginLoader
from .skill_parser import SkillLoader, SkillDefinition

if TYPE_CHECKING:
    from sherry_agent.infrastructure.tools.base import BaseTool, ToolDefinition


class PluginManager:
    """插件管理器"""

    def __init__(self, plugin_dirs: Optional[List[str]] = None, skill_dirs: Optional[List[str]] = None):
        self.loader = PluginLoader(plugin_dirs)
        self.skill_dirs = skill_dirs or []
        self._initialized = False
        self._loaded_skills: List[SkillDefinition] = []

    def initialize(self) -> None:
        """初始化插件系统"""
        if not self._initialized:
            self.loader.load_all()
            self._register_plugin_tools()
            self._load_skills()
            self._initialized = True

    def _load_skills(self) -> None:
        """加载技能"""
        for skill_dir in self.skill_dirs:
            skills = SkillLoader.load_skills_from_directory(skill_dir)
            self._loaded_skills.extend(skills)

    def get_skills(self) -> List[SkillDefinition]:
        """获取所有已加载的技能"""
        return self._loaded_skills.copy()

    def load_skill(self, skill_path: str) -> Optional[SkillDefinition]:
        """加载单个技能"""
        skill = SkillLoader.load_skill(skill_path)
        if skill:
            self._loaded_skills.append(skill)
            return skill
        return None

    def load_skills_from_directory(self, directory: str) -> List[SkillDefinition]:
        """从目录加载技能"""
        skills = SkillLoader.load_skills_from_directory(directory)
        self._loaded_skills.extend(skills)
        return skills

    def _register_plugin_tools(self) -> None:
        """注册插件提供的工具"""
        try:
            print("=== 开始注册插件工具 ===")
            
            # 直接调用每个插件的 get_tools 方法
            for plugin_name, plugin in self.loader.get_loaded_plugins().items():
                print(f"处理插件: {plugin_name}")
                try:
                    if hasattr(plugin, 'get_tools'):
                        tools = plugin.get_tools()
                        print(f"  插件 {plugin_name} 提供了 {len(tools)} 个工具")
                        for i, tool_obj in enumerate(tools):
                            print(f"  工具 {i+1}:")
                            print(f"    类型: {type(tool_obj)}")
                            print(f"    所有属性: {dir(tool_obj)}")
                            
                            # 尝试直接访问属性
                            try:
                                print(f"    名称: {getattr(tool_obj, 'name', '未知')}")
                                print(f"    描述: {getattr(tool_obj, 'description', '未知')}")
                                print(f"    参数: {getattr(tool_obj, 'parameters', '未知')}")
                                print(f"    权限: {getattr(tool_obj, 'permissions', '未知')}")
                                print(f"    执行方法: {getattr(tool_obj, 'execute', '未知')}")
                            except Exception as e:
                                print(f"    访问属性时出错: {e}")
                            
                            # 尝试注册工具
                            try:
                                # 直接创建 ToolDefinition
                                tool_name = getattr(tool_obj, 'name', f'tool_{i}')
                                tool_description = getattr(tool_obj, 'description', '未知工具')
                                tool_parameters = getattr(tool_obj, 'parameters', {})
                                tool_permissions = getattr(tool_obj, 'permissions', [])
                                tool_execute = getattr(tool_obj, 'execute', None)
                                
                                if tool_execute:
                                    tool_def = ToolDefinition(
                                        name=tool_name,
                                        description=tool_description,
                                        parameters=tool_parameters,
                                        permissions=tool_permissions,
                                        func=tool_execute,
                                    )
                                    _TOOL_REGISTRY[tool_name] = tool_def
                                    print(f"    成功注册工具: {tool_name}")
                                else:
                                    print(f"    无法注册工具: 缺少 execute 方法")
                            except Exception as e:
                                print(f"    注册工具时出错: {e}")
                except Exception as e:
                    print(f"  处理插件 {plugin_name} 时出错: {e}")
            
            print(f"=== 插件工具注册完成，共注册 {len(_TOOL_REGISTRY)} 个工具 ===")
        except Exception as e:
            print(f"Error registering plugin tools: {e}")

    def get_plugins(self) -> Dict[str, Plugin]:
        """获取所有已加载的插件"""
        return self.loader.get_loaded_plugins()

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """根据名称获取插件"""
        return self.loader.get_loaded_plugins().get(name)

    def load_plugin(self, plugin_path: str) -> Optional[Plugin]:
        """加载单个插件"""
        # 尝试从目录加载
        plugins = self.loader.load_from_directory(plugin_path)
        if plugins:
            self._register_plugin_tools()
            return plugins[0]
        return None

    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        result = self.loader.unload_plugin(plugin_name)
        # 注意：这里没有从工具注册表中移除插件提供的工具
        # 因为可能有其他插件也提供了相同名称的工具
        return result

    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件"""
        return self.loader.enable_plugin(plugin_name)

    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件"""
        return self.loader.disable_plugin(plugin_name)

    def is_plugin_enabled(self, plugin_name: str) -> bool:
        """检查插件是否启用"""
        return self.loader.is_plugin_enabled(plugin_name)

    def get_enabled_plugins(self) -> List[Plugin]:
        """获取所有启用的插件"""
        return self.loader.get_enabled_plugins()

    def reload_plugins(self) -> List[Plugin]:
        """重新加载所有插件"""
        self.loader.clear()
        plugins = self.loader.load_all()
        self._register_plugin_tools()
        return plugins

    def trigger_agent_started(self, agent_id: str, config: Dict[str, Any]) -> None:
        """触发 Agent 启动事件"""
        try:
            plugin_hooks.hook.agent_started(agent_id=agent_id, config=config)
        except Exception as e:
            print(f"Error triggering agent_started hook: {e}")

    def trigger_agent_stopped(self, agent_id: str, status: str) -> None:
        """触发 Agent 停止事件"""
        try:
            plugin_hooks.hook.agent_stopped(agent_id=agent_id, status=status)
        except Exception as e:
            print(f"Error triggering agent_stopped hook: {e}")

    def shutdown(self) -> None:
        """关闭插件系统"""
        self.loader.clear()
        self._loaded_skills.clear()
        self._initialized = False


# 创建全局插件管理器实例
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager(plugin_dirs: Optional[List[str]] = None, skill_dirs: Optional[List[str]] = None) -> PluginManager:
    """获取全局插件管理器实例"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager(plugin_dirs=plugin_dirs, skill_dirs=skill_dirs)
    return _plugin_manager


from sherry_agent.config.settings import settings

def initialize_plugins() -> None:
    """初始化插件系统"""
    manager = get_plugin_manager(plugin_dirs=settings.plugin_dirs, skill_dirs=settings.skill_dirs)
    manager.initialize()
