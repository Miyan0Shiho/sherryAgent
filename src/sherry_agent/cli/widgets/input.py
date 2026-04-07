
from textual.widgets import Input


class UserInput(Input):
    """用户输入组件"""

    def __init__(self, id: str | None = None, prompt: str = "> "):
        super().__init__(id=id, placeholder="输入任务指令...")
        self.prompt = prompt

    def on_mount(self) -> None:
        """组件挂载时的初始化"""
        self.focus()

    def get_user_input(self) -> str:
        """获取用户输入"""
        value = self.value.strip()
        self.value = ""
        return value

    def set_placeholder(self, placeholder: str) -> None:
        """设置占位符"""
        self.placeholder = placeholder
