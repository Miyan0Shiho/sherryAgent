import os
import requests
from sherry_agent.plugins.sdk import BaseTool


class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "weather"
    
    @property
    def description(self) -> str:
        return "查询天气信息"
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    
    async def execute(self, city: str) -> dict:
        api_key = os.getenv("API_KEY", "test_key")
        # 模拟天气 API 响应
        return {
            "city": city,
            "temperature": 25,
            "condition": "晴天",
            "humidity": 60,
            "wind_speed": 10
        }
