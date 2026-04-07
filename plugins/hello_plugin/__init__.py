from sherry_agent.plugins.sdk import BasePlugin, BaseTool, plugin
from sherry_agent.infrastructure.tools.base import Permission, ToolResult

class HelloTool(BaseTool):
    @property
    def name(self) -> str:
        return "hello"
    
    @property
    def description(self) -> str:
        return "向世界问好"
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "要问候的名字"
                }
            },
            "required": ["name"]
        }
    
    @property
    def permissions(self) -> list:
        return []
    
    async def execute(self, **kwargs) -> ToolResult:
        name = kwargs.get("name")
        result = f"Hello, {name}! Welcome to SherryAgent!"
        return ToolResult(
            success=True,
            content=result,
            metadata={"name": name}
        )


@plugin
class HelloPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "hello-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "一个示例插件，提供问候功能"
    
    def get_tools(self) -> list:
        return [HelloTool()]
