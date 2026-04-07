"""
Pytest配置

定义测试夹具和配置。
"""

import pytest
import sys
from pathlib import Path

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_llm_response():
    """模拟LLM响应"""
    return {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": "Test response"}],
    }
