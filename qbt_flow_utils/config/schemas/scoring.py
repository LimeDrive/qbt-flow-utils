"""Scoring Config Schema"""
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ScoreCalculationConfig(BaseModel):
    coef_day_seed_time: float = 0.5
    coef_seed_ratio: int = 2
    coef_nums_seeder: float = 0.1


class ScoringConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ignore_untagged_torrents: bool = True
    ignore_tags_for_selection: Optional[List[str]] = None
    extra_tags_score: Optional[Dict[str, int]] = None
    score_calculation: ScoreCalculationConfig
