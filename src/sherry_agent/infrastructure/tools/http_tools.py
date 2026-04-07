
import aiohttp

from .base import Permission, ToolResult, tool


@tool(
    name="http_request",
    description="发送 HTTP 请求",
    parameters={
        "url": {
            "type": "string",
            "description": "请求 URL",
        },
        "method": {
            "type": "string",
            "description": "HTTP 方法（GET、POST、PUT、DELETE 等）",
        },
        "headers": {
            "type": "object",
            "description": "请求头",
        },
        "body": {
            "type": "string",
            "description": "请求体",
        },
    },
    permissions=[Permission.NETWORK],
)
async def http_request(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: str | None = None,
) -> ToolResult:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                data=body,
            ) as response:
                response_text = await response.text()

                return ToolResult(
                    success=response.status < 400,
                    content=response_text,
                    metadata={
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "url": str(response.url),
                    },
                )
    except Exception as e:
        return ToolResult(
            success=False,
            content=f"HTTP request failed: {e}",
            metadata={"url": url, "method": method},
        )
