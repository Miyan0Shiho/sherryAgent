from typing import Any

import aiohttp

from .base import BaseTool, Permission, ToolResult


class HttpTool(BaseTool):
    @property
    def name(self) -> str:
        return "http_request"

    @property
    def description(self) -> str:
        return "发送 HTTP 请求"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "url": {
                "type": "string",
                "description": "请求的 URL",
            },
            "method": {
                "type": "string",
                "description": "HTTP 方法",
                "default": "GET",
                "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            },
            "headers": {
                "type": "object",
                "description": "请求头",
                "default": {},
            },
            "data": {
                "type": "object",
                "description": "请求数据",
                "default": {},
            },
            "timeout": {
                "type": "integer",
                "description": "请求超时时间（秒）",
                "default": 30,
            }
        }

    @property
    def permissions(self) -> list[Permission]:
        return [Permission.NETWORK]

    async def execute(self, **kwargs: Any) -> ToolResult:
        try:
            # 获取参数
            url = kwargs.get("url", "")
            method = kwargs.get("method", "GET")
            headers = kwargs.get("headers", {})
            data = kwargs.get("data", {})
            timeout = kwargs.get("timeout", 30)

            # 确保 headers 和 data 不为 None
            headers = headers or {}
            data = data or {}

            # 发送请求
            async with aiohttp.ClientSession() as session:
                # 根据方法选择请求函数
                method = method.upper()
                request_kwargs = {
                    "url": url,
                    "headers": headers,
                    "timeout": aiohttp.ClientTimeout(total=timeout),
                }

                if method in ["POST", "PUT", "PATCH"]:
                    request_kwargs["json"] = data

                # 发送请求
                if method == "GET":
                    async with session.get(**request_kwargs) as response:
                        content = await response.text()
                elif method == "POST":
                    async with session.post(**request_kwargs) as response:
                        content = await response.text()
                elif method == "PUT":
                    async with session.put(**request_kwargs) as response:
                        content = await response.text()
                elif method == "DELETE":
                    async with session.delete(**request_kwargs) as response:
                        content = await response.text()
                elif method == "PATCH":
                    async with session.patch(**request_kwargs) as response:
                        content = await response.text()
                else:
                    return ToolResult(
                        success=False,
                        content=f"Unsupported HTTP method: {method}",
                        metadata={"url": url, "method": method},
                    )

                # 构建结果
                success = 200 <= response.status < 300
                metadata: dict[str, Any] = {
                    "status": response.status,
                    "url": url,
                    "method": method,
                    "headers": dict(response.headers),
                    "timeout": timeout,
                }

                return ToolResult(
                    success=success,
                    content=content,
                    metadata=metadata,
                )
        except aiohttp.ClientError as e:
            return ToolResult(
                success=False,
                content=f"HTTP client error: {e}",
                metadata={"url": url, "method": method, "timeout": timeout},
            )
        except TimeoutError:
            return ToolResult(
                success=False,
                content=f"Request timed out after {timeout} seconds",
                metadata={"url": url, "method": method, "timeout": timeout},
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=f"Error sending HTTP request: {e}",
                metadata={"url": url, "method": method, "timeout": timeout},
            )
