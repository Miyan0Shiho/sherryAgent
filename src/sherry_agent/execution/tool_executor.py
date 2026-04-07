"""Abstract base class for tool executors."""

from abc import ABC, abstractmethod
from typing import Any


class ToolExecutor(ABC):
    """Abstract base class for tool executors."""

    @abstractmethod
    async def execute_tool(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        call_id: str,
    ) -> tuple[str, dict[str, Any]]:
        """Execute a tool with the given parameters.

        Args:
            tool_name: Name of the tool to execute.
            tool_input: Input parameters for the tool.
            call_id: Unique identifier for this tool call.

        Returns:
            Tuple of (result_content, result_metadata).
        """
        pass
