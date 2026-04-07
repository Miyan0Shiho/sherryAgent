#!/usr/bin/env python3
"""
测试 TUI 输出
"""

import subprocess
import time


def test_tui_output():
    """测试 TUI 输出"""
    print("=== 测试 TUI 输出 ===")
    
    # 启动 TUI 并捕获输出
    process = subprocess.Popen(
        ['uv', 'run', 'sherry-agent', 'run', '--model', 'qwen3:0.6b'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    try:
        # 读取输出
        output = []
        start_time = time.time()
        
        while time.time() - start_time < 5:  # 等待 5 秒
            line = process.stdout.readline()
            if line:
                output.append(line)
                print(f"输出: {line.rstrip()}")
            else:
                time.sleep(0.1)
        
        print("\n✅ TUI 启动输出已捕获")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    finally:
        # 终止进程
        process.terminate()
        try:
            process.wait(timeout=2)
        except:
            process.kill()
        print("✅ TUI 已关闭")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_tui_output()
