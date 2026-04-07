
from textual.app import App, ComposeResult
from textual.events import Key
from textual.widgets import Input

from ..config import settings
from ..execution.agent_loop import agent_loop
from ..infrastructure.tool_executor import ToolExecutor
from ..llm import AnthropicClient, LLMClient, MockLLMClient, OpenAIClient, OllamaClient
from ..models.config import AgentConfig
from ..models.events import AgentEvent, EventType
from .widgets import StatusBar, TerminalOutput, UserInput


def create_llm_client(model: str) -> LLMClient:
    """根据模型名称创建对应的 LLM 客户端"""
    if model.startswith("claude-"):
        if settings.anthropic_api_key:
            return AnthropicClient(api_key=settings.anthropic_api_key)
        else:
            return MockLLMClient(
                responses=["请先在 .env 文件中配置 ANTHROPIC_API_KEY"]
            )
    elif model.startswith("gpt-") or model.startswith("o1-"):
        if settings.openai_api_key:
            return OpenAIClient(api_key=settings.openai_api_key)
        else:
            return MockLLMClient(
                responses=["请先在 .env 文件中配置 OPENAI_API_KEY"]
            )
    else:
        # 假设其他模型都是 Ollama 本地模型
        return OllamaClient()


class SherryAgentTUI(App[None]):
    """SherryAgent TUI 界面"""

    CSS = """
    #terminal-container {
        height: 80%;
        border: solid green;
        background: black;
        color: white;
    }

    #terminal-content {
        padding: 1;
    }

    UserInput {
        height: 3;
        border: solid green;
        background: black;
        color: white;
    }

    #status-bar {
        height: 3;
        border: solid green;
        background: black;
        color: white;
        padding: 0 1;
    }

    #status-indicator {
        width: 30%;
    }

    #model-indicator {
        width: 40%;
    }

    #debug-indicator {
        width: 30%;
    }
    """

    def __init__(self, model: str, debug: bool):
        super().__init__()
        self.model = model
        self._debug = debug
        self.agent_task = None
        self._is_running = False
        self.llm_client = create_llm_client(model)
        self.tool_executor = ToolExecutor()
        self.config = AgentConfig(model=model)
        self.messages: list[dict[str, str]] = []

    def compose(self) -> ComposeResult:
        yield TerminalOutput(id="terminal-output")
        yield UserInput(id="user-input")
        yield StatusBar(id="status-bar")

    def on_mount(self) -> None:
        """界面挂载时的初始化"""
        self.title = "SherryAgent"
        self.terminal = self.query_one("#terminal-output", TerminalOutput)
        self.user_input = self.query_one("#user-input", UserInput)
        self.status_bar = self.query_one("#status-bar", StatusBar)

        self.status_bar.update_model(self.model)
        self.status_bar.update_debug(self._debug)

        self.terminal.add_line("SherryAgent v0.1.0")
        self.terminal.add_line(f"模型: {self.model}")
        self.terminal.add_line(f"调试模式: {'开启' if self._debug else '关闭'}")
        self.terminal.add_line("\n输入任务指令开始交互，按 Ctrl+C 中止任务")
        self.terminal.add_line("-" * 80)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """处理用户输入"""
        user_input = event.value.strip()
        if not user_input or self._is_running:
            return

        self.terminal.add_line(f"> {user_input}")
        self.status_bar.update_status("处理中...")
        self._is_running = True

        self.messages.append({"role": "user", "content": user_input})

        self.run_worker(self.run_agent_task(user_input), exclusive=True)

    async def run_agent_task(self, task: str) -> None:
        """运行 Agent 任务"""
        try:
            async for event in agent_loop(
                messages=self.messages,
                config=self.config,
                llm_client=self.llm_client,
                tool_executor=self.tool_executor,
            ):
                if event.event_type == EventType.TEXT:
                    self.terminal.append_text(event.content)
                elif event.event_type == EventType.TOOL_USE:
                    self.terminal.add_line(f"\n🔧 调用工具: {event.content}")
                elif event.event_type == EventType.TOOL_RESULT:
                    self.terminal.add_line(f"✅ 工具结果: {event.content}")
                elif event.event_type == EventType.ERROR:
                    self.terminal.add_line(f"❌ 错误: {event.content}")

            self.terminal.add_line("\n" + "-" * 80)
            self.status_bar.update_status("就绪")
        except Exception as e:
            self.terminal.add_line(f"\n❌ 执行错误: {str(e)}")
            self.status_bar.update_status("就绪")
        finally:
            self._is_running = False

    def on_key(self, event: Key) -> None:
        """处理键盘事件"""
        if event.key == "ctrl+c":
            if self._is_running:
                self.terminal.add_line("\n⚠️  任务已中止")
                self.status_bar.update_status("就绪")
                self._is_running = False
                event.stop()
