import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

UTC = timezone.utc


class HeartbeatStatusManager:
    """心跳状态管理器，处理 HEARTBEAT.md 的读写"""

    def __init__(self, file_path: str = "HEARTBEAT.md"):
        self.file_path = file_path

    def read_status(self) -> Dict[str, Any]:
        """读取 HEARTBEAT.md 文件"""
        if not os.path.exists(self.file_path):
            return self._create_default_status()

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析 Markdown 内容
            status = self._parse_markdown(content)
            return status
        except Exception as e:
            print(f"Error reading HEARTBEAT.md: {e}")
            return self._create_default_status()

    def write_status(self, status: Dict[str, Any]) -> None:
        """写入 HEARTBEAT.md 文件"""
        try:
            content = self._generate_markdown(status)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing HEARTBEAT.md: {e}")

    def _create_default_status(self) -> Dict[str, Any]:
        """创建默认状态"""
        return {
            "mode": "normal",
            "last_heartbeat": datetime.now(UTC).isoformat(),
            "cycle_count": 0,
            "pending_tasks": [],
            "cron_schedule": [],
            "recent_activity": []
        }

    def _parse_markdown(self, content: str) -> Dict[str, Any]:
        """解析 Markdown 内容"""
        status = self._create_default_status()

        # 简单解析，实际项目中可能需要更复杂的解析
        lines = content.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            
            if line.startswith('## '):
                current_section = line[3:].strip()
            elif current_section == "Current Mode":
                if line.startswith('- Mode: '):
                    status["mode"] = line[8:].strip()
                elif line.startswith('- Last Heartbeat: '):
                    status["last_heartbeat"] = line[18:].strip()
                elif line.startswith('- Cycle Count: '):
                    try:
                        status["cycle_count"] = int(line[14:].strip())
                    except:
                        pass
            elif current_section == "Pending Tasks":
                if line.startswith('- [ ] '):
                    task = line[6:].strip()
                    status["pending_tasks"].append(task)
            elif current_section == "Cron Schedule":
                # 跳过表头和分隔线
                if not line.startswith('|') or line.startswith('|------') or 'Task' in line and 'Schedule' in line:
                    continue
                if line.startswith('|'):
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 3:
                        status["cron_schedule"].append({
                            "task": parts[0],
                            "schedule": parts[1],
                            "next_run": parts[2]
                        })
            elif current_section == "Recent Activity":
                if line.startswith('- '):
                    activity = line[2:].strip()
                    status["recent_activity"].append(activity)

        return status

    def _generate_markdown(self, status: Dict[str, Any]) -> str:
        """生成 Markdown 内容"""
        sections = []

        # Current Mode
        sections.append("# Agent Heartbeat Status\n")
        sections.append("## Current Mode")
        sections.append(f"- Mode: {status.get('mode', 'normal')}")
        sections.append(f"- Last Heartbeat: {status.get('last_heartbeat', datetime.now(UTC).isoformat())}")
        sections.append(f"- Cycle Count: {status.get('cycle_count', 0)}")
        sections.append("")

        # Pending Tasks
        sections.append("## Pending Tasks")
        for task in status.get('pending_tasks', []):
            sections.append(f"- [ ] {task}")
        sections.append("")

        # Cron Schedule
        sections.append("## Cron Schedule")
        sections.append("| Task | Schedule | Next Run |")
        sections.append("|------|----------|----------|")
        for item in status.get('cron_schedule', []):
            sections.append(f"| {item.get('task', '')} | {item.get('schedule', '')} | {item.get('next_run', '')} |")
        sections.append("")

        # Recent Activity
        sections.append("## Recent Activity")
        for activity in status.get('recent_activity', []):
            sections.append(f"- {activity}")
        sections.append("")

        return '\n'.join(sections)

    def add_pending_task(self, task: str) -> None:
        """添加待办任务"""
        status = self.read_status()
        if task not in status.get('pending_tasks', []):
            status['pending_tasks'].append(task)
            self.write_status(status)

    def remove_pending_task(self, task: str) -> None:
        """移除待办任务"""
        status = self.read_status()
        if task in status.get('pending_tasks', []):
            status['pending_tasks'].remove(task)
            self.write_status(status)

    def add_activity(self, activity: str) -> None:
        """添加活动记录"""
        status = self.read_status()
        timestamp = datetime.now(UTC).isoformat()
        status['recent_activity'].insert(0, f"{timestamp}: {activity}")
        # 只保留最近 10 条活动记录
        status['recent_activity'] = status['recent_activity'][:10]
        self.write_status(status)
