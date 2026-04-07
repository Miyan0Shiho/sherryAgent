
"""
配置管理模块

使用 pydantic-settings 加载配置和环境变量。
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class HeartbeatSettings(BaseSettings):
    """心跳引擎配置"""
    base_interval: int = 60
    low_power_interval: int = 300
    idle_threshold: int = 5
    max_concurrent_tasks: int = 3


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    anthropic_api_key: str = ""
    openai_api_key: str = ""
    default_model: str = "qwen3:0.6b"
    environment: str = "development"
    heartbeat: HeartbeatSettings = HeartbeatSettings()
    plugin_dirs: list[str] = ["plugins"]
    skill_dirs: list[str] = ["skills"]


settings = Settings()
