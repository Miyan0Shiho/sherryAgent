from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:  # Python 3.11+
    import tomllib  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]

from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


def _read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    return data if isinstance(data, dict) else {}


class TomlLayerSettingsSource(PydanticBaseSettingsSource):
    """Load optional TOML layers with deterministic precedence."""

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._cache: dict[str, Any] | None = None

    def _load(self) -> dict[str, Any]:
        if self._cache is not None:
            return self._cache

        repo_root = Path(os.getenv("SHERRY_AGENT_REPO_ROOT") or Path.cwd()).expanduser()
        config_dir = Path(os.getenv("SHERRY_AGENT_CONFIG_DIR") or (repo_root / ".sherryagent")).expanduser()
        candidates = [
            config_dir / "settings.default.toml",
            config_dir / "settings.toml",
            Path.home() / ".config" / "sherry-agent" / "settings.toml",
        ]

        repo_toml = os.getenv("SHERRY_AGENT_REPO_TOML")
        user_toml = os.getenv("SHERRY_AGENT_USER_TOML")
        runtime_toml = os.getenv("SHERRY_AGENT_RUNTIME_TOML")
        if repo_toml:
            candidates.append(Path(repo_toml).expanduser())
        if user_toml:
            candidates.append(Path(user_toml).expanduser())
        if runtime_toml:
            candidates.append(Path(runtime_toml).expanduser())

        merged: dict[str, Any] = {}
        for path in candidates:
            merged.update(_read_toml(path))
        self._cache = merged
        return merged

    def __call__(self) -> dict[str, Any]:
        return self._load()

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        data = self._load()
        if field_name in data:
            return data[field_name], field_name, False
        return None, field_name, False


class Settings(BaseSettings):
    """Layered configuration for the foundation/persistence slice."""

    model_config = SettingsConfigDict(
        env_prefix="SHERRY_AGENT_",
        extra="ignore",
        case_sensitive=False,
    )

    environment: str = "local"
    repo_root: Path = Field(default_factory=Path.cwd)
    config_dir: Path | None = None
    data_dir: Path | None = None
    db_path: Path | None = None
    default_mode: str = "interactive-dev"
    default_budget_profile: str = "balanced"
    strict_budget_profile: str = "strict"
    balanced_budget_profile: str = "balanced"
    premium_budget_profile: str = "premium"
    memory_short_ttl_hours: int = 24
    memory_work_ttl_days: int = 7
    memory_long_ttl_days: int = 90
    sqlite_foreign_keys: bool = True
    allow_background_writes: bool = False
    max_tool_calls: int = 12
    max_parallel_tools: int = 4
    story_work_unit_prefix: str = "codex/multi-agent-test"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            TomlLayerSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )

    @property
    def resolved_repo_root(self) -> Path:
        return self.repo_root.expanduser().resolve()

    @property
    def resolved_config_dir(self) -> Path:
        if self.config_dir is not None:
            return self.config_dir.expanduser().resolve()
        return self.resolved_repo_root / ".sherryagent"

    @property
    def resolved_data_dir(self) -> Path:
        if self.data_dir is not None:
            return self.data_dir.expanduser().resolve()
        return self.resolved_config_dir

    @property
    def database_path(self) -> Path:
        if self.db_path is not None:
            return self.db_path.expanduser().resolve()
        return self.resolved_data_dir / "sherry-agent.sqlite3"

    @property
    def runtime_override_path(self) -> Path:
        return self.resolved_config_dir / "settings.runtime.toml"

    @property
    def repo_override_path(self) -> Path:
        return self.resolved_config_dir / "settings.toml"

    @property
    def user_override_path(self) -> Path:
        return Path.home() / ".config" / "sherry-agent" / "settings.toml"

    def config_layer_paths(self) -> tuple[Path, Path, Path, Path]:
        return (
            self.resolved_config_dir / "settings.default.toml",
            self.repo_override_path,
            self.user_override_path,
            self.runtime_override_path,
        )


AppSettings = Settings


def load_settings(workspace_root: str = ".") -> Settings:
    return Settings(repo_root=Path(workspace_root))


__all__ = ["AppSettings", "Settings", "TomlLayerSettingsSource", "load_settings"]
