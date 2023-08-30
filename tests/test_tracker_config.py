# tests/test_tracker_config.py
import pytest
from pydantic import ValidationError

from qbt_flow_utils.config.schemas.trackers import TrackerConfig


def test_valid_tracker_config():
    valid_config = {
        "tracker_tag": "pytest",
        "tracker_keywords": ["example.com", "key.example.com"],
        "extra_score": 1000,
        "hit_and_run": {
            "ignore_hit_and_run": False,
            "min_seed_time": 40,
            "min_ratio": 1,
        },
        "auto_manage": {
            "conditions": {
                "max_seed_time": 30,
                "max_ratio": 2,
                "min_active_seeder": 2,
                "protect_hit_and_run": False,
            },
            "action": {
                "limit_upload_speed": 512,
            },
        },
    }
    TrackerConfig.model_validate(valid_config)


def test_invalid_tracker_config():
    invalid_config = {
        "tracker_tag": "pytest",
        "tracker_keywords": ["example.com"],
        "extra_score": 1000,
        "hit_and_run": {
            "ignore_hit_and_run": False,
        },
        "auto_manage": {
            "conditions": {
                "max_seed_time": 30,
                "max_ratio": 2,
                "min_active_seeder": 2,
                "protect_hit_and_run": False,
            },
            "action": {
                "limit_upload_speed": "512kbps",  # Invalid value
            },
        },
    }
    with pytest.raises(ValidationError):
        TrackerConfig.model_validate(invalid_config)
