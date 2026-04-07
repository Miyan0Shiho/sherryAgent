"""
CLI入口点

提供命令行界面入口。
"""

import click
import os
import sys
import time
from typing import Optional

from .tui import SherryAgentTUI
from sherry_agent.autonomy import HeartbeatEngine
from sherry_agent.plugins import initialize_plugins
from sherry_agent.plugins.manager import get_plugin_manager


@click.group()
@click.version_option(version="0.1.0", prog_name="sherry-agent")
def cli() -> None:
    """
    SherryAgent - 基于 Claude Code 与 OpenClaw 融合的 Python 多 Agent 框架
    """
    pass


def _daemonize() -> None:
    """将进程 daemon 化"""
    # 第一次 fork
    try:
        pid = os.fork()
        if pid > 0:
            # 父进程退出
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"fork #1 failed: {e}\n")
        sys.exit(1)

    # 脱离控制终端
    os.setsid()

    # 第二次 fork
    try:
        pid = os.fork()
        if pid > 0:
            # 父进程退出
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"fork #2 failed: {e}\n")
        sys.exit(1)

    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()

    # 关闭所有文件描述符
    for fd in range(3):
        try:
            os.close(fd)
        except OSError:
            pass

    # 打开 /dev/null 作为标准输入、输出和错误
    os.open(os.devnull, os.O_RDWR)  # stdin
    os.dup2(0, 1)  # stdout
    os.dup2(0, 2)  # stderr


@cli.command()
@click.option("--model", default="claude-sonnet-4-20250514", help="LLM模型")
@click.option("--debug", is_flag=True, help="启用调试模式")
@click.option("--daemon", is_flag=True, help="后台运行模式")
def run(model: str, debug: bool, daemon: bool) -> None:
    """启动交互式Agent会话"""
    # 初始化插件系统
    initialize_plugins()
    
    if daemon:
        _daemonize()
        click.echo("SherryAgent 已在后台启动")
        # 启动心跳引擎
        engine = HeartbeatEngine()
        import asyncio
        asyncio.run(engine.start())
    else:
        tui = SherryAgentTUI(model=model, debug=debug)
        tui.run()


@cli.command()
def status() -> None:
    """显示Agent状态"""
    click.echo("SherryAgent 状态:")
    click.echo("  - 核心Agent Loop: ✅ 已完成")
    click.echo("  - 记忆系统: ✅ 已完成")
    click.echo("  - 自主运行: 🔄 开发中")
    click.echo("    - 心跳引擎: ✅ 已完成")
    click.echo("    - Cron调度: ✅ 已完成")
    click.echo("    - 后台模式: ✅ 已完成")
    click.echo("    - WebSocket: 📝 规划中")
    click.echo("    - 低功耗模式: 📝 规划中")
    click.echo("  - 多Agent编排: 📝 规划中")
    click.echo("  - 插件生态: ✅ 已完成")


@cli.group()
def plugin() -> None:
    """插件管理命令"""
    pass


@plugin.command()
def list() -> None:
    """列出所有已加载的插件"""
    initialize_plugins()
    manager = get_plugin_manager()
    plugins = manager.get_plugins()
    
    if not plugins:
        click.echo("没有加载任何插件")
        return
    
    click.echo("已加载的插件:")
    click.echo("-" * 80)
    for name, plugin in plugins.items():
        status = "启用" if manager.is_plugin_enabled(name) else "禁用"
        click.echo(f"名称: {name}")
        click.echo(f"版本: {plugin.version}")
        click.echo(f"描述: {plugin.description}")
        click.echo(f"状态: {status}")
        click.echo("-" * 80)


@plugin.command()
@click.argument("plugin_name")
def enable(plugin_name: str) -> None:
    """启用指定插件"""
    initialize_plugins()
    manager = get_plugin_manager()
    
    if manager.get_plugin(plugin_name):
        if manager.enable_plugin(plugin_name):
            click.echo(f"插件 {plugin_name} 已成功启用")
        else:
            click.echo(f"插件 {plugin_name} 启用失败")
    else:
        click.echo(f"插件 {plugin_name} 不存在")


@plugin.command()
@click.argument("plugin_name")
def disable(plugin_name: str) -> None:
    """禁用指定插件"""
    initialize_plugins()
    manager = get_plugin_manager()
    
    if manager.get_plugin(plugin_name):
        if manager.disable_plugin(plugin_name):
            click.echo(f"插件 {plugin_name} 已成功禁用")
        else:
            click.echo(f"插件 {plugin_name} 禁用失败")
    else:
        click.echo(f"插件 {plugin_name} 不存在")


def main() -> None:
    """CLI主入口"""
    cli()


if __name__ == "__main__":
    main()
