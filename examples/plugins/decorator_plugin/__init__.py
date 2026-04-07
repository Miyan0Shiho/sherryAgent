from sherry_agent.plugins.sdk import BasePlugin, plugin, tool
import requests


@plugin
class DecoratorPlugin(BasePlugin):
    """使用装饰器定义工具的示例插件"""
    
    @property
    def name(self) -> str:
        return "decorator-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "使用装饰器定义工具的示例插件"
    
    @property
    def dependencies(self) -> list:
        return ["requests"]
    
    @tool(
        name="get_joke",
        description="获取一个笑话",
        parameters={
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "笑话类别",
                    "enum": ["general", "programming", "knock-knock"]
                }
            },
            "required": ["category"]
        }
    )
    async def get_joke(self, category: str) -> str:
        """获取指定类别的笑话"""
        url = f"https://api.chucknorris.io/jokes/random?category={category}"
        response = requests.get(url)
        data = response.json()
        return data["value"]
    
    @tool(
        name="get_weather",
        description="获取城市天气",
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    )
    async def get_weather(self, city: str) -> dict:
        """获取指定城市的天气信息"""
        # 注意：这里使用的是一个免费的天气API，可能会有请求限制
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        return response.json()
    
    def get_tools(self) -> list:
        """从类中提取装饰的工具"""
        tools = []
        for name in dir(self):
            attr = getattr(self, name)
            if hasattr(attr, "__tool_name__"):
                from sherry_agent.plugins.sdk.tools import ToolDefinition
                tool_def = ToolDefinition(
                    name=attr.__tool_name__,
                    description=attr.__tool_description__,
                    parameters=attr.__tool_parameters__,
                    permissions=attr.__tool_permissions__,
                    func=attr
                )
                tools.append(tool_def)
        return tools
    
    def agent_started(self, agent_id: str, config: dict) -> None:
        """Agent启动时触发"""
        print(f"DecoratorPlugin: Agent {agent_id} started")
    
    def agent_stopped(self, agent_id: str, status: str) -> None:
        """Agent停止时触发"""
        print(f"DecoratorPlugin: Agent {agent_id} stopped with status {status}")
