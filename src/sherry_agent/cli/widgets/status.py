
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static


class StatusBar(Static):
    """状态显示组件"""

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self._status = "就绪"
        self._model = ""
        self._debug = False

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Static("状态: 就绪", id="status-indicator"),
            Static("模型: ", id="model-indicator"),
            Static("调试: 关闭", id="debug-indicator"),
            id="status-bar"
        )

    def update_status(self, status: str) -> None:
        """更新状态"""
        self._status = status
        status_indicator = self.query_one("#status-indicator", Static)
        status_indicator.update(f"状态: {status}")

    def update_model(self, model: str) -> None:
        """更新模型信息"""
        self._model = model
        model_indicator = self.query_one("#model-indicator", Static)
        model_indicator.update(f"模型: {model}")

    def update_debug(self, debug: bool) -> None:
        """更新调试模式"""
        self._debug = debug
        debug_indicator = self.query_one("#debug-indicator", Static)
        debug_indicator.update(f"调试: {'开启' if debug else '关闭'}")
