#!/usr/bin/env python3
"""
测试 Ollama 本地模型集成
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from sherry_agent.llm import OllamaClient


async def test_ollama_integration():
    """测试 Ollama 本地模型集成"""
    print("=== 测试 Ollama 本地模型集成 ===")
    
    # 创建 Ollama 客户端
    client = OllamaClient()
    print("✅ 创建 Ollama 客户端成功")
    
    # 测试简单的聊天功能
    messages = [
        {"role": "user", "content": "你好，请介绍一下自己"}
    ]
    
    try:
        print("🔄 发送请求到本地 Ollama 模型...")
        response = await client.chat(
            messages=messages,
            model="qwen3:0.6b",
            max_tokens=1000
        )
        
        print("✅ 收到模型响应:")
        print(response)
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_ollama_integration())
