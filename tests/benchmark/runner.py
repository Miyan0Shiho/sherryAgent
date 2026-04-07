#!/usr/bin/env python3
"""
Benchmark Runner - 测试执行引擎
集成 SherryAgent 的 Agent Loop，配置使用 ollama 的 qwen3:0.6b 模型
实现完整的执行日志记录
"""

import asyncio
import json
import logging
import sys
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from sherry_agent.execution.agent_loop import agent_loop, ToolExecutor
from sherry_agent.infrastructure.tool_executor import ToolExecutor as ConcreteToolExecutor
from sherry_agent.llm.client import OllamaClient, LLMClient
from sherry_agent.models.config import AgentConfig
from sherry_agent.models.events import AgentEvent, EventType

from tests.benchmark.logger import ExecutionLogger


class BenchmarkStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TestCase:
    test_id: str
    name: str
    description: str
    user_prompt: str
    system_prompt: str = ""
    expected_output: Optional[str] = None
    max_tokens: int = 2048
    timeout: float = 300.0


@dataclass
class ExecutionLog:
    timestamp: datetime
    event_type: EventType
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    token_usage: Optional[dict[str, int]] = None


@dataclass
class BenchmarkResult:
    test_id: str
    status: BenchmarkStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    execution_logs: list[ExecutionLog] = field(default_factory=list)
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    error_message: Optional[str] = None
    final_response: Optional[str] = None
    log_files: Optional[dict[str, str]] = None


class BenchmarkRunner:
    """基准测试执行器，负责执行测试用例并记录执行日志"""

    def __init__(
        self,
        model: str = "qwen3:0.6b",
        ollama_base_url: str = "http://localhost:11434",
        log_dir: str = "tests/benchmark/logs",
        max_tokens: int = 2048,
        max_tool_rounds: int = 10,
        token_budget: int = 100_000,
    ):
        self.model = model
        self.ollama_base_url = ollama_base_url
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_tokens = max_tokens
        self.max_tool_rounds = max_tool_rounds
        self.token_budget = token_budget
        
        self.llm_client: LLMClient = OllamaClient(base_url=ollama_base_url)
        self.tool_executor: ToolExecutor = ConcreteToolExecutor()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _create_agent_config(self, test_case: TestCase) -> AgentConfig:
        """创建 Agent 配置，使用 qwen3:0.6b 模型"""
        tools = self.tool_executor.get_available_tools()
        return AgentConfig(
            model=self.model,
            max_tokens=test_case.max_tokens or self.max_tokens,
            max_tool_rounds=self.max_tool_rounds,
            token_budget=self.token_budget,
            system_prompt=test_case.system_prompt,
            tools=tools,
        )

    async def run_test(self, test_case: TestCase) -> BenchmarkResult:
        """执行单个测试用例"""
        self.logger.info(f"开始执行测试: {test_case.test_id} - {test_case.name}")
        
        start_time = datetime.now()
        result = BenchmarkResult(
            test_id=test_case.test_id,
            status=BenchmarkStatus.RUNNING,
            start_time=start_time,
        )
        
        execution_logger = ExecutionLogger(self.log_dir, run_id=test_case.test_id)
        
        try:
            messages = [
                {"role": "user", "content": test_case.user_prompt}
            ]
            
            config = self._create_agent_config(test_case)
            
            execution_logger.start_execution(
                task_id=test_case.test_id,
                config={
                    "model": config.model,
                    "max_tokens": config.max_tokens,
                    "max_tool_rounds": config.max_tool_rounds,
                    "token_budget": config.token_budget,
                }
            )
            
            async for event in execution_logger.consume_events(
                agent_loop(
                    messages=messages,
                    config=config,
                    llm_client=self.llm_client,
                    tool_executor=self.tool_executor,
                )
            ):
                execution_log = self._record_event(event)
                result.execution_logs.append(execution_log)
                
                if event.event_type == EventType.TEXT and event.content:
                    result.final_response = event.content
                
                if event.token_usage:
                    result.input_tokens += event.token_usage.input_tokens
                    result.output_tokens += event.token_usage.output_tokens
                    result.total_tokens += (
                        event.token_usage.input_tokens + 
                        event.token_usage.output_tokens
                    )
                
                if event.event_type == EventType.ERROR:
                    result.status = BenchmarkStatus.FAILED
                    result.error_message = event.content
            
            if result.status == BenchmarkStatus.RUNNING:
                result.status = BenchmarkStatus.COMPLETED
                execution_logger.end_execution(True, "Test completed successfully")
            else:
                execution_logger.end_execution(False, result.error_message or "Test failed")
            
            self.logger.info(f"测试执行完成: {test_case.test_id}, 状态: {result.status.value}")
            
        except Exception as e:
            result.status = BenchmarkStatus.FAILED
            result.error_message = str(e)
            execution_logger.log_error(e, "Test execution failed")
            execution_logger.end_execution(False, str(e))
            self.logger.error(f"测试执行失败: {test_case.test_id}, 错误: {str(e)}")
        finally:
            result.end_time = datetime.now()
            result.log_files = {
                "json": str(execution_logger.json_log_path),
                "text": str(execution_logger.text_log_path),
            }
            self._save_result(result)
        
        return result

    def _record_event(self, event: AgentEvent) -> ExecutionLog:
        """记录执行事件"""
        token_usage_dict = None
        if event.token_usage:
            token_usage_dict = {
                "input_tokens": event.token_usage.input_tokens,
                "output_tokens": event.token_usage.output_tokens,
                "cache_read_tokens": event.token_usage.cache_read_tokens,
                "cache_creation_tokens": event.token_usage.cache_creation_tokens,
            }
        
        return ExecutionLog(
            timestamp=datetime.now(),
            event_type=event.event_type,
            content=event.content,
            metadata=event.metadata,
            token_usage=token_usage_dict,
        )

    def _save_result(self, result: BenchmarkResult) -> None:
        """保存测试结果到文件"""
        timestamp = result.start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"{result.test_id}_summary_{timestamp}.json"
        filepath = self.log_dir / filename
        
        result_dict = {
            "test_id": result.test_id,
            "status": result.status.value,
            "start_time": result.start_time.isoformat(),
            "end_time": result.end_time.isoformat() if result.end_time else None,
            "total_tokens": result.total_tokens,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
            "error_message": result.error_message,
            "final_response": result.final_response,
            "log_files": result.log_files,
            "execution_logs": [
                {
                    "timestamp": log.timestamp.isoformat(),
                    "event_type": log.event_type.value,
                    "content": log.content,
                    "metadata": log.metadata,
                    "token_usage": log.token_usage,
                }
                for log in result.execution_logs
            ],
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"测试结果已保存到: {filepath}")

    async def run_multiple_tests(self, test_cases: list[TestCase]) -> list[BenchmarkResult]:
        """批量执行多个测试用例"""
        results = []
        for test_case in test_cases:
            result = await self.run_test(test_case)
            results.append(result)
        return results


def create_simple_test_case(
    test_id: str,
    name: str,
    user_prompt: str,
    system_prompt: str = "",
    max_tokens: int = 1024,
) -> TestCase:
    """创建简单的测试用例"""
    return TestCase(
        test_id=test_id,
        name=name,
        description=f"测试用例: {name}",
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
    )
