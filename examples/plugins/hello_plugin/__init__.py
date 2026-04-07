from sherry_agent.plugins.sdk import BasePlugin, BaseTool, plugin


class HelloTool(BaseTool):
    """问候工具"""
    
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
    
    async def execute(self, name: str) -> str:
        """执行问候操作"""
        return f"Hello, {name}! Welcome to SherryAgent!"


class CalculatorTool(BaseTool):
    """计算器工具"""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "执行基本数学计算"
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "操作类型",
                    "enum": ["add", "subtract", "multiply", "divide"]
                },
                "a": {
                    "type": "number",
                    "description": "第一个操作数"
                },
                "b": {
                    "type": "number",
                    "description": "第二个操作数"
                }
            },
            "required": ["operation", "a", "b"]
        }
    
    async def execute(self, operation: str, a: float, b: float) -> float:
        """执行计算操作"""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("除数不能为零")
            return a / b
        else:
            raise ValueError(f"不支持的操作: {operation}")


@plugin
class HelloPlugin(BasePlugin):
    """示例插件"""
    
    @property
    def name(self) -> str:
        return "hello-plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "一个示例插件，提供问候和计算功能"
    
    @property
    def dependencies(self) -> list:
        return []
    
    def get_tools(self) -> list:
        """获取插件提供的工具"""
        return [HelloTool(), CalculatorTool()]
    
    def agent_started(self, agent_id: str, config: dict) -> None:
        """Agent启动时触发"""
        print(f"HelloPlugin: Agent {agent_id} started with model {config.get('model', 'unknown')}")
    
    def agent_stopped(self, agent_id: str, status: str) -> None:
        """Agent停止时触发"""
        print(f"HelloPlugin: Agent {agent_id} stopped with status {status}")
