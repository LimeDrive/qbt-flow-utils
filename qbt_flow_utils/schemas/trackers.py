from datetime import timedelta
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ByteSize, ConfigDict, Field, RootModel, model_validator

from .utils import parse_time


class HitAndRunConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    ignore_hit_and_run: bool = True
    min_seed_time: Optional[timedelta] = None
    min_ratio: Optional[float] = None

    @model_validator(mode="before")
    @classmethod
    def validate_conditions(cls, values: Any) -> Any:
        ignore_hit_and_run = values.get("ignore_hit_and_run", True)
        min_seed_time = values.get("min_seed_time")
        min_ratio = values.get("min_ratio")

        if min_seed_time is not None:
            values["min_seed_time"] = parse_time(min_seed_time)

        if not ignore_hit_and_run and (min_seed_time is None) and (min_ratio is None):
            raise ValueError(
                "If ignore_hit_and_run is set to False, either min_seed_time or min_ratio must"
                " be provided",
            )

        return values


class AutoManageConditions(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_seed_time: Optional[timedelta] = None
    max_ratio: Optional[float] = None
    min_active_seeder: Optional[int] = None
    protect_hit_and_run: bool = False


class AutoManageAction(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    limit_upload_speed: Optional[ByteSize] = None
    pause_torrent: Optional[bool] = None
    stop_torrent: Optional[bool] = None
    move_to_local: Optional[bool] = None
    sync_to_remote: Optional[bool] = None
    remove_torrent: Optional[bool] = None

    @model_validator(mode="before")
    @classmethod
    # TODO:LOW review validate_single_action validator
    def validate_single_action(cls, values: Any) -> Any:
        actions = [
            values.get(field)
            for field in [
                "limit_upload_speed",
                "pause_torrent",
                "stop_torrent",
                "move_to_local",
                "sync_to_remote",
                "remove_torrent",
            ]
        ]
        true_actions = [action for action in actions if action is True]

        if len(true_actions) > 1:
            raise ValueError("Only one action can be set to True")

        return values


class AutoManageConfig(BaseModel):
    conditions: Optional[AutoManageConditions]
    action: Optional[AutoManageAction]


class TrackerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    tracker_tag: str = Field(pattern=r"^[A-Za-z0-9_-]{2,}$")
    extra_score: int = Field(ge=0, default=0)
    tracker_keywords: List[str]
    hit_and_run: HitAndRunConfig
    auto_manage: Optional[AutoManageConfig]


class TrackersConfig(RootModel[Dict[str, TrackerConfig]]):
    root: Dict[str, TrackerConfig]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def get_items(self):
        yield from self.root.items()
