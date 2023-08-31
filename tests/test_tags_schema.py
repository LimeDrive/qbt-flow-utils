# tests/test_tags_schema.py
import pytest
from pydantic import ValidationError

from qbt_flow_utils.schemas.tags import TagsConfig


def test_valid_tags_config():
    valid_config = {
        "auto_tags_no_hard_link": True,
        "no_hard_link_tag": "noHL",
        "auto_tags_hard_link": True,
        "hard_link_tag": "HardLink",
        "auto_tags_hit_and_run": True,
        "hit_and_run_tag": "H&R",
        "auto_tags_upload_limit": True,
        "upload_limit_tag": "UpLimit",
        "auto_tags_public": True,
        "public_tag": "Public",
        "auto_tags_unknown_trackers": True,
        "unknown_tracker_tag": "Other",
    }
    TagsConfig.model_validate(valid_config)


def test_invalid_tags_config():
    invalid_config = {
        "auto_tags_no_hard_link": True,
        "no_hard_link_tag": "noHL",
        "auto_tags_hard_link": True,
        "hard_link_tag": "HardLink",
        "auto_tags_hit_and_run": True,
        "hit_and_run_tag": "",
        "auto_tags_upload_limit": True,
        "upload_limit_tag": "UpLimit",
        "auto_tags_public": True,
        "public_tag": "Public",
        "auto_tags_unknown_trackers": True,
        "unknown_tracker_tag": "Other",
    }
    with pytest.raises(ValidationError):
        TagsConfig.model_validate(invalid_config)
