"""Settings for qbt_flow_utils package."""
import enum
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """Application settings.

    This parameters can be configured
    with environment variables.
    """

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for qbt-flow-utils @TODO: review command names
    dry_run: bool = False
    deamon_mode: bool = False
    auto_manage: bool = False
    auto_tags: bool = True
    auto_remove: bool = True
    auto_sync: bool = False
    auto_move: bool = False
    check_hard_links: bool = True
    check_cross_seed: bool = True

    # Variables for Redis
    redis_host: str = "qfu-redis"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None

    # Path variables
    root_path: str = "/app"  # Absolute Path to root folder
    config_folder: str = (  # Absolute path of config folder TODO: dev propose
        "/root/qbt-flow-utils/config"
    )
    download_folder: str = "/downloads"  # Path to download folder
    media_folder: str = "/media"  # Path to media folder

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="QFU_",
        env_file_encoding="utf-8",
    )


settings = Settings()

# Path: qbt_flow_utils/settings.py
