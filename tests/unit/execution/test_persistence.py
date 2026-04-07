import os
import shutil
import tempfile
import pytest
from src.sherry_agent.execution.persistence import (
    TaskStatus, TaskState, TranscriptEntry, TaskPersistence, RecoveryContext
)
from datetime import datetime


class TestTaskPersistence:
    """测试任务持久化功能"""

    def setup_method(self):
        """设置测试环境"""
        # 创建临时目录作为任务目录
        self.temp_dir = tempfile.mkdtemp()
        self.persistence = TaskPersistence(tasks_dir=self.temp_dir)
        self.task_id = "test-task-123"

    def teardown_method(self):
        """清理测试环境"""
        # 删除临时目录
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_create_task(self):
        """测试创建任务"""
        task = await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task",
            parent_task_id="parent-123"
        )

        assert task.task_id == self.task_id
        assert task.description == "Test task"
        assert task.status == TaskStatus.PENDING
        assert task.parent_task_id == "parent-123"

        # 验证状态文件已创建
        state_file = self.persistence.get_state_file(self.task_id)
        assert os.path.exists(state_file)

        # 验证心跳文件已创建
        heartbeat_file = self.persistence.get_heartbeat_file(self.task_id)
        assert os.path.exists(heartbeat_file)

    async def test_save_and_load_state(self):
        """测试保存和加载任务状态"""
        # 创建任务
        task = await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task"
        )

        # 更新状态
        task.status = TaskStatus.RUNNING
        task.current_step = 1
        task.total_steps = 5
        task.progress = 20.0

        # 保存状态
        await self.persistence.save_state(task)

        # 加载状态
        loaded_task = await self.persistence.load_state(self.task_id)

        assert loaded_task is not None
        assert loaded_task.task_id == self.task_id
        assert loaded_task.status == TaskStatus.RUNNING
        assert loaded_task.current_step == 1
        assert loaded_task.total_steps == 5
        assert loaded_task.progress == 20.0

    async def test_append_and_load_transcript(self):
        """测试追加和加载执行日志"""
        # 创建任务
        await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task"
        )

        # 追加日志条目
        entry1 = TranscriptEntry(
            timestamp=datetime.now(),
            step_index=0,
            event_type="user_input",
            content="Hello",
            token_usage={"prompt_tokens": 10, "completion_tokens": 5},
            duration_ms=100
        )

        entry2 = TranscriptEntry(
            timestamp=datetime.now(),
            step_index=1,
            event_type="agent_output",
            content="Hi there",
            token_usage={"prompt_tokens": 15, "completion_tokens": 8},
            duration_ms=150
        )

        await self.persistence.append_transcript(self.task_id, entry1)
        await self.persistence.append_transcript(self.task_id, entry2)

        # 加载日志
        entries = await self.persistence.load_transcript(self.task_id)

        assert len(entries) == 2
        assert entries[0].event_type == "user_input"
        assert entries[0].content == "Hello"
        assert entries[1].event_type == "agent_output"
        assert entries[1].content == "Hi there"

    async def test_update_heartbeat(self):
        """测试更新心跳信息"""
        # 创建任务
        await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task"
        )

        # 更新心跳
        await self.persistence.update_heartbeat(self.task_id, "Test heartbeat")

        # 读取心跳文件
        heartbeat_file = self.persistence.get_heartbeat_file(self.task_id)
        with open(heartbeat_file, "r") as f:
            content = f.read()

        assert "Test heartbeat" in content

    async def test_scan_interrupted_tasks(self):
        """测试扫描中断的任务"""
        # 创建两个任务
        task1 = await self.persistence.create_task(
            task_id="task-1",
            description="Task 1"
        )

        task2 = await self.persistence.create_task(
            task_id="task-2",
            description="Task 2"
        )

        # 更新任务状态
        await self.persistence.update_task_status("task-1", TaskStatus.RUNNING)
        await self.persistence.update_task_status("task-2", TaskStatus.COMPLETED)

        # 扫描中断的任务
        interrupted_tasks = await self.persistence.scan_interrupted_tasks()

        assert len(interrupted_tasks) == 1
        assert interrupted_tasks[0].task_id == "task-1"
        assert interrupted_tasks[0].status == TaskStatus.RUNNING

    async def test_recover_task(self):
        """测试从断点恢复任务"""
        # 创建任务
        await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task"
        )

        # 追加日志条目
        await self.persistence.append_transcript(self.task_id, TranscriptEntry(
            timestamp=datetime.now(),
            step_index=0,
            event_type="user_input",
            content="Hello"
        ))

        await self.persistence.append_transcript(self.task_id, TranscriptEntry(
            timestamp=datetime.now(),
            step_index=0,
            event_type="step_started",
            content="Processing step 1"
        ))

        await self.persistence.append_transcript(self.task_id, TranscriptEntry(
            timestamp=datetime.now(),
            step_index=0,
            event_type="agent_output",
            content="Hi there"
        ))

        await self.persistence.append_transcript(self.task_id, TranscriptEntry(
            timestamp=datetime.now(),
            step_index=0,
            event_type="step_completed",
            content="Step 1 completed"
        ))

        await self.persistence.append_transcript(self.task_id, TranscriptEntry(
            timestamp=datetime.now(),
            step_index=1,
            event_type="step_started",
            content="Processing step 2"
        ))

        # 更新任务状态为 RUNNING
        await self.persistence.update_task_status(self.task_id, TaskStatus.RUNNING)

        # 恢复任务
        recovery_context = await self.persistence.recover_task(self.task_id)

        assert recovery_context is not None
        assert recovery_context.task_state.task_id == self.task_id
        assert len(recovery_context.messages) == 2
        assert recovery_context.messages[0]["role"] == "user"
        assert recovery_context.messages[0]["content"] == "Hello"
        assert recovery_context.messages[1]["role"] == "agent"
        assert recovery_context.messages[1]["content"] == "Hi there"
        assert recovery_context.last_successful_step == 0
        assert len(recovery_context.pending_steps) == 1
        assert recovery_context.pending_steps[0] == "Processing step 2"

    async def test_update_task_status(self):
        """测试更新任务状态"""
        # 创建任务
        await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task"
        )

        # 更新状态为 RUNNING
        updated_task = await self.persistence.update_task_status(
            self.task_id, TaskStatus.RUNNING
        )

        assert updated_task is not None
        assert updated_task.status == TaskStatus.RUNNING

        # 更新状态为 FAILED
        updated_task = await self.persistence.update_task_status(
            self.task_id, TaskStatus.FAILED, "Test error"
        )

        assert updated_task is not None
        assert updated_task.status == TaskStatus.FAILED
        assert updated_task.error_message == "Test error"

    async def test_update_task_progress(self):
        """测试更新任务进度"""
        # 创建任务
        await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task"
        )

        # 更新进度
        updated_task = await self.persistence.update_task_progress(
            self.task_id, current_step=2, total_steps=5, progress=40.0
        )

        assert updated_task is not None
        assert updated_task.current_step == 2
        assert updated_task.total_steps == 5
        assert updated_task.progress == 40.0

    async def test_complete_task(self):
        """测试完成任务"""
        # 创建任务
        await self.persistence.create_task(
            task_id=self.task_id,
            description="Test task"
        )

        # 完成任务
        updated_task = await self.persistence.complete_task(
            self.task_id, "Task completed successfully"
        )

        assert updated_task is not None
        assert updated_task.status == TaskStatus.COMPLETED
        assert updated_task.result_summary == "Task completed successfully"
        assert updated_task.progress == 100.0
        assert updated_task.completed_at is not None

    async def test_load_nonexistent_state(self):
        """测试加载不存在的任务状态"""
        state = await self.persistence.load_state("nonexistent-task")
        assert state is None

    async def test_load_nonexistent_transcript(self):
        """测试加载不存在的执行日志"""
        entries = await self.persistence.load_transcript("nonexistent-task")
        assert len(entries) == 0

    async def test_recover_nonexistent_task(self):
        """测试恢复不存在的任务"""
        recovery_context = await self.persistence.recover_task("nonexistent-task")
        assert recovery_context is None


if __name__ == "__main__":
    pytest.main([__file__])
