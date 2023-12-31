"""Tags validation schema."""
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)


class TagsConfig(BaseModel):
    """Tags validation schema."""

    model_config = ConfigDict(extra="forbid")

    auto_tags_no_hard_link: bool = False
    no_hard_link_tag: str = "noHL"

    # hardlinks torrents
    auto_tags_hard_link: bool = False
    hard_link_tag: str = "HardLink"

    # Hit-and-Run torrents
    auto_tags_hit_and_run: bool = False
    hit_and_run_tag: str = "H&R"

    # Up limit by auto-manage or manual
    auto_tags_upload_limit: bool = False
    upload_limit_tag: str = "UpLimit"

    # Public tracker Torrents
    auto_tags_public: bool = False
    public_tag: str = "Public"

    # False configured tracker tags
    auto_tags_unknown_trackers: bool = False
    unknown_tracker_tag: str = "Other"

    @model_validator(mode="before")
    @classmethod
    def validate_tags_string(cls, values: Any) -> Any:
        """Validate tags string."""
        for field in [
            "no_hard_link_tag",
            "hard_link_tag",
            "hit_and_run_tag",
            "upload_limit_tag",
            "public_tag",
            "unknown_tracker_tag",
        ]:
            if values.get(field) == "":
                raise ValueError(f"{field} cannot be empty")

        return values
