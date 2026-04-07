from __future__ import annotations

import importlib
import importlib.metadata
import os
import sys
from typing import Dict, List, Optional, Set, Type, Any

from .hooks import Plugin, plugin_hooks


class PluginLoader:
    """插件加载器"""

    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        self.plugin_dirs = plugin_dirs or []
        self.loaded_plugins: Dict[str, Plugin] = {}
        self.enabled_plugins: Set[str] = set()
        self.plugin_dependencies: Dict[str, List[str]] = {}

    def load_from_directory(self, directory: str) -> List[Plugin]:
        """从目录加载插件"""
        loaded: List[Plugin] = []
        if not os.path.exists(directory):
            return loaded

        # 添加目录到 Python 路径
        if directory not in sys.path:
            sys.path.insert(0, directory)

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, "__init__.py")):
                # 加载目录作为模块
                try:
                    module_name = item
                    module = importlib.import_module(module_name)
                    plugin = self._extract_plugin(module)
                    if plugin:
                        self._load_plugin(plugin)
                        loaded.append(plugin)
                except Exception as e:
                    print(f"Failed to load plugin from {item_path}: {e}")
            elif item.endswith(".py") and item != "__init__.py":
                # 加载单个 Python 文件
                try:
                    module_name = item[:-3]
                    module = importlib.import_module(module_name)
                    plugin = self._extract_plugin(module)
                    if plugin:
                        self._load_plugin(plugin)
                        loaded.append(plugin)
                except Exception as e:
                    print(f"Failed to load plugin from {item_path}: {e}")

        return loaded

    def load_from_entry_points(self) -> List[Plugin]:
        """从 entry points 加载插件"""
        loaded: List[Plugin] = []
        try:
            entry_points = importlib.metadata.entry_points()
            if hasattr(entry_points, 'select'):
                # Python 3.10+
                for entry_point in entry_points.select(group="sherry_agent.plugins"):
                    try:
                        plugin = entry_point.load()
                        if isinstance(plugin, type):
                            plugin_instance = plugin()
                        else:
                            plugin_instance = plugin
                        if isinstance(plugin_instance, Plugin):
                            self._load_plugin(plugin_instance)
                            loaded.append(plugin_instance)
                    except Exception as e:
                        print(f"Failed to load plugin from entry point {entry_point.name}: {e}")
            else:
                # Python 3.9 及以下
                for entry_point in entry_points.get("sherry_agent.plugins", []):  # type: ignore[attr-defined]
                    try:
                        plugin = entry_point.load()
                        if isinstance(plugin, type):
                            plugin_instance = plugin()
                        else:
                            plugin_instance = plugin
                        if isinstance(plugin_instance, Plugin):
                            self._load_plugin(plugin_instance)
                            loaded.append(plugin_instance)
                    except Exception as e:
                        print(f"Failed to load plugin from entry point {entry_point.name}: {e}")
        except Exception as e:
            print(f"Error loading entry points: {e}")
        return loaded

    def load_all(self) -> List[Plugin]:
        """加载所有插件"""
        loaded = []
        for directory in self.plugin_dirs:
            loaded.extend(self.load_from_directory(directory))
        loaded.extend(self.load_from_entry_points())
        return loaded

    def _extract_plugin(self, module: Any) -> Optional[Plugin]:
        """从模块中提取插件实例"""
        for name in dir(module):
            obj = getattr(module, name)
            # 检查是否是 Plugin 实例但不是类本身
            if isinstance(obj, Plugin) and not isinstance(obj, type):
                print(f"Found plugin instance: {obj.name}")
                return obj
            elif isinstance(obj, type):
                # 检查是否实现了 Plugin 协议的所有必要属性
                try:
                    if all(hasattr(obj, attr) for attr in ['name', 'version', 'description']):
                        try:
                            plugin_instance = obj()
                            # 验证实例是否真正实现了 Plugin 协议
                            if isinstance(plugin_instance, Plugin):
                                print(f"Created plugin instance: {plugin_instance.name}")
                                return plugin_instance
                        except Exception as e:
                            print(f"Failed to instantiate plugin {obj.__name__}: {e}")
                except Exception as e:
                    print(f"Error checking plugin class {obj.__name__}: {e}")
        return None

    def _load_plugin(self, plugin: Plugin) -> None:
        """加载插件到插件管理器"""
        plugin_name = str(plugin.name)
        if plugin_name not in self.loaded_plugins:
            # 检查并加载依赖
            if hasattr(plugin, 'dependencies'):
                self.plugin_dependencies[plugin_name] = plugin.dependencies
                # 这里可以添加依赖解析逻辑
            
            plugin_hooks.register(plugin)
            self.loaded_plugins[plugin_name] = plugin
            self.enabled_plugins.add(plugin_name)
            # 触发插件加载钩子
            plugin_hooks.hook.plugin_loaded(plugin=plugin)

    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        if plugin_name in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_name]
            plugin_hooks.unregister(plugin)
            # 触发插件卸载钩子
            plugin_hooks.hook.plugin_unloaded(plugin=plugin)
            del self.loaded_plugins[plugin_name]
            return True
        return False

    def get_loaded_plugins(self) -> Dict[str, Plugin]:
        """获取已加载的插件"""
        return self.loaded_plugins.copy()

    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件"""
        if plugin_name in self.loaded_plugins:
            self.enabled_plugins.add(plugin_name)
            # 触发插件启用钩子
            if hasattr(plugin_hooks.hook, 'plugin_enabled'):
                plugin_hooks.hook.plugin_enabled(plugin=self.loaded_plugins[plugin_name])
            return True
        return False

    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件"""
        if plugin_name in self.loaded_plugins:
            self.enabled_plugins.discard(plugin_name)
            # 触发插件禁用钩子
            if hasattr(plugin_hooks.hook, 'plugin_disabled'):
                plugin_hooks.hook.plugin_disabled(plugin=self.loaded_plugins[plugin_name])
            return True
        return False

    def is_plugin_enabled(self, plugin_name: str) -> bool:
        """检查插件是否启用"""
        return plugin_name in self.enabled_plugins

    def get_enabled_plugins(self) -> List[Plugin]:
        """获取所有启用的插件"""
        return [plugin for name, plugin in self.loaded_plugins.items() if name in self.enabled_plugins]

    def clear(self) -> None:
        """清空所有加载的插件"""
        for plugin_name in list(self.loaded_plugins.keys()):
            self.unload_plugin(plugin_name)
        self.enabled_plugins.clear()
        self.plugin_dependencies.clear()
