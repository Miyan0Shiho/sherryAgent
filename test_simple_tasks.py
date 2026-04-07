#!/usr/bin/env python3
"""
测试 SherryAgent 执行简单任务的能力
"""

import asyncio
from src.sherry_agent.llm.client import OllamaClient

async def test_simple_tasks():
    """测试简单任务"""
    print("测试 SherryAgent 执行简单任务的能力...\n")
    
    # 创建 Ollama 客户端
    client = OllamaClient()
    
    # 测试任务列表
    test_tasks = [
        {"role": "user", "content": "你好，今天天气怎么样？"},
        {"role": "user", "content": "123 + 456 等于多少？"},
        {"role": "user", "content": "什么是人工智能？"}
    ]
    
    for i, task in enumerate(test_tasks):
        print(f"测试 {i+1}: {task['content']}")
        
        try:
            # 发送请求
            response = await client.chat(
                messages=[task],
                model="qwen3:0.6b",
                max_tokens=200,
                system_prompt="你是一个 helpful 的 AI 助手"
            )
            
            print("✅ 任务完成！")
            print("响应:")
            print(response.content)
            print("-" * 50)
        except Exception as e:
            print(f"❌ 任务失败: {str(e)}")
            print("-" * 50)
    
    print("简单任务测试完成！")

if __name__ == "__main__":
    asyncio.run(test_simple_tasks())