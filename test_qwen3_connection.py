#!/usr/bin/env python3
"""
测试 SherryAgent 与 qwen3:0.6b 模型的连接
"""

import asyncio
from src.sherry_agent.llm.client import OllamaClient

async def test_qwen3_connection():
    """测试与 qwen3:0.6b 模型的连接"""
    print("测试 SherryAgent 与 qwen3:0.6b 模型的连接...")
    
    # 创建 Ollama 客户端
    client = OllamaClient()
    
    # 测试基本对话
    messages = [
        {"role": "user", "content": "你好，你是谁？"}
    ]
    
    try:
        # 发送请求
        response = await client.chat(
            messages=messages,
            model="qwen3:0.6b",
            max_tokens=100,
            system_prompt="你是一个 helpful 的 AI 助手"
        )
        
        print("✅ 连接成功！")
        print("模型响应:")
        print(response.content)
        print("\nToken 使用:")
        print(f"输入 tokens: {response.token_usage.input_tokens}")
        print(f"输出 tokens: {response.token_usage.output_tokens}")
        
        return True
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_qwen3_connection())