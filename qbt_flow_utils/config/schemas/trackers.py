from typing import Any, List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)


class HitAndRunConfig(BaseModel):
    ignore_hit_and_run: bool = True
    min_seed_time: Optional[int]
    min_ratio: Optional[float]

    @model_validator(mode="before")
    @classmethod
    def validate_conditions(cls, values: Any) -> Any:
        ignore_hit_and_run = values.get("ignore_hit_and_run", True)
        min_seed_time = values.get("min_seed_time")
        min_ratio = values.get("min_ratio")

        if not ignore_hit_and_run and (min_seed_time is None) and (min_ratio is None):
            raise ValueError(
                "If ignore_hit_and_run is set to False, either min_seed_time or min_ratio must be provided",
            )

        return values


class AutoManageConditions(BaseModel):
    max_seed_time: Optional[int] = None
    max_ratio: Optional[float] = None
    min_active_seeder: Optional[int] = None
    protect_hit_and_run: bool = False


class AutoManageAction(BaseModel):
    limit_upload_speed: Optional[int] = None
    pause_torrent: Optional[bool] = None
    stop_torrent: Optional[bool] = None
    move_to_local: Optional[bool] = None
    sync_to_remote: Optional[bool] = None
    remove_torrent: Optional[bool] = None

    @model_validator(mode="before")
    @classmethod
    def validate_single_action(cls, values: Any) -> Any:
        actions = [
            values.get(field)
            for field in [
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
    model_config = ConfigDict(extra="forbid")

    extra_score: int = 0
    tracker_keywords: List[str]
    hit_and_run: HitAndRunConfig
    auto_manage: Optional[AutoManageConfig]
