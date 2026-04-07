
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.scroll_view import ScrollView
from textual.widgets import Static


class TerminalOutput(ScrollView):
    """终端输出组件"""

    def __init__(self, id: str | None = None):
        super().__init__(id=id)
        self._output_lines: list[str] = []

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(id="terminal-content"),
            id="terminal-container"
        )

    def add_line(self, line: str) -> None:
        """添加一行输出"""
        self._output_lines.append(line)
        self.update_output()

    def add_multiple_lines(self, lines: list[str]) -> None:
        """添加多行输出"""
        self._output_lines.extend(lines)
        self.update_output()

    def update_output(self) -> None:
        """更新输出内容"""
        content = self.query_one("#terminal-content", Static)
        content.update("\n".join(self._output_lines))
        self.scroll_end()

    def clear(self) -> None:
        """清空输出"""
        self._output_lines = []
        self.update_output()
