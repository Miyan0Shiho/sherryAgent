#!/usr/bin/env python3
"""
自动测试 TUI 交互功能
"""

import pexpect
import time
import sys


def test_tui_interaction():
    """测试 TUI 交互功能"""
    print("=== 测试 TUI 交互功能 ===")
    
    # 启动 TUI
    child = pexpect.spawn('uv run sherry-agent run --model qwen3:0.6b', encoding='utf-8')
    
    try:
        # 等待 TUI 启动完成
        child.expect('输入任务指令开始交互', timeout=10)
        print("✅ TUI 启动成功")
        
        # 等待提示符
        time.sleep(1)
        
        # 发送测试输入
        test_input = "你好"
        print(f"🔄 发送输入: {test_input}")
        child.sendline(test_input)
        
        # 等待响应
        print("🔄 等待模型响应...")
        # 等待至少 20 秒，因为模型可能需要一些时间来响应
        try:
            # 等待分隔线，表示响应完成
            child.expect('------------------------------', timeout=20)
            print("✅ 收到模型响应")
        except pexpect.TIMEOUT:
            print("⚠️  响应超时，检查是否有输出...")
            # 打印当前输出
            print("当前输出:")
            print(child.before)
            
        # 检查是否有错误信息
        if '错误' in child.before:
            print("❌ 发现错误信息")
        else:
            print("✅ 没有错误信息")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 终止 TUI
        child.sendcontrol('c')
        try:
            child.expect(pexpect.EOF, timeout=5)
        except:
            pass
        print("✅ TUI 已关闭")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_tui_interaction()
