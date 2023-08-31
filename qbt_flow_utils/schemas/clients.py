import re
from typing import Any, Dict, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class ClientLoginConfig(BaseModel):
    host: str
    port: Optional[int] = Field(None, ge=1, le=65535)
    username: str
    password: str
    VERIFY_WEBUI_CERTIFICATE: bool = False
    RAISE_ERROR_FOR_UNSUPPORTED_QBITTORRENT_VERSIONS: bool = True
    RAISE_NOTIMPLEMENTEDERROR_FOR_UNIMPLEMENTED_API_ENDPOINTS: bool = True


class ClientDiskControlMethodConfig(BaseModel):
    max_percents: Optional[int] = None
    path_to_check: Optional[str] = None
    keep_free_gib: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def validate_disk_control_condition(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if (values.get("max_percents") is None) and (values.get("keep_free_gib") is None):
                raise ValueError(
                    "Either max_percents or keep_free_gib must be provided",
                )

            if (values.get("max_percents") is not None) and (
                values.get("keep_free_gib") is not None
            ):
                raise ValueError(
                    "Either max_percents or keep_free_gib must be provided, not both",
                )

            if (values.get("max_percents") is not None) and (values.get("path_to_check") is None):
                raise ValueError(
                    "path_to_check must be provided if max_percents is provided",
                )

            if values.get("max_percents") is not None and (
                values["max_percents"] <= 5 or values["max_percents"] >= 95
            ):
                raise ValueError(
                    "max_percents must be between 5 and 95",
                )

            if values.get("keep_free_gib") is not None and values["keep_free_gib"] <= 5:
                raise ValueError(
                    "keep_free_gib must be greater than 5",
                )
        else:
            raise TypeError(
                "Disk control method must be difined in clients config",
            )

        return values


class ClientPathConfig(BaseModel):
    downloads_path: str
    recycle_bin: str


class ClientConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: ClientLoginConfig
    disk_control_method: ClientDiskControlMethodConfig
    category: Optional[Dict[str, str]] = None
    path: ClientPathConfig

    @model_validator(mode="after")
    def validate_absolute_path(self) -> "ClientConfig":
        if self.category:
            for category in self.category.values():
                if not re.match(r"^/", category):
                    raise ValueError(
                        f"Category {category} must be an absolute path",
                    )

        for path in [self.path.downloads_path, self.path.recycle_bin]:
            if not re.match(r"^/", path):
                raise ValueError(
                    f"Path {path} must be an absolute path",
                )

        if self.disk_control_method.path_to_check and not re.match(
            r"^/",
            self.disk_control_method.path_to_check,
        ):
            raise ValueError(
                f"Path {self.disk_control_method.path_to_check} must be an absolute path",
            )

        return self
