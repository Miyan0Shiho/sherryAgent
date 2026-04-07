import tempfile
from pathlib import Path

import pytest
from src.sherry_agent.infrastructure.tools.file_tools import read_file, write_file, _resolve_path, SandboxError


@pytest.fixture
def sandbox_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_resolve_path_inside_sandbox(sandbox_dir):
    target_path = _resolve_path("test.txt", sandbox_dir)
    assert target_path == (sandbox_dir / "test.txt").resolve()


def test_resolve_path_outside_sandbox(sandbox_dir):
    with pytest.raises(SandboxError):
        _resolve_path("../outside.txt", sandbox_dir)


def test_resolve_path_absolute_path(sandbox_dir):
    with pytest.raises(SandboxError):
        _resolve_path("/etc/passwd", sandbox_dir)


@pytest.mark.asyncio
async def test_write_and_read_file(sandbox_dir, monkeypatch):
    monkeypatch.setattr(
        "src.sherry_agent.infrastructure.tools.file_tools._get_sandbox_root",
        lambda: sandbox_dir,
    )

    test_content = "Hello, World!"
    test_path = "test.txt"

    write_result = await write_file(test_path, test_content)
    assert write_result.success is True

    read_result = await read_file(test_path)
    assert read_result.success is True
    assert read_result.content == test_content


@pytest.mark.asyncio
async def test_read_nonexistent_file(sandbox_dir, monkeypatch):
    monkeypatch.setattr(
        "src.sherry_agent.infrastructure.tools.file_tools._get_sandbox_root",
        lambda: sandbox_dir,
    )

    result = await read_file("nonexistent.txt")
    assert result.success is False
    assert "File not found" in result.content


@pytest.mark.asyncio
async def test_sandbox_protection_read(sandbox_dir, monkeypatch):
    monkeypatch.setattr(
        "src.sherry_agent.infrastructure.tools.file_tools._get_sandbox_root",
        lambda: sandbox_dir,
    )

    result = await read_file("../outside.txt")
    assert result.success is False
    assert "Security error" in result.content


@pytest.mark.asyncio
async def test_sandbox_protection_write(sandbox_dir, monkeypatch):
    monkeypatch.setattr(
        "src.sherry_agent.infrastructure.tools.file_tools._get_sandbox_root",
        lambda: sandbox_dir,
    )

    result = await write_file("../outside.txt", "test")
    assert result.success is False
    assert "Security error" in result.content
