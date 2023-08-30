"""Configuration files for qbt_flow_utils."""
from qbt_flow_utils.config.config import (
    get_clients_config,
    get_clients_list,
    get_scoring_config,
    get_tags_config,
    get_trackers_config,
    get_trackers_tags,
)

QFUTrackerConfig = get_trackers_config
QFUTrackerList = get_trackers_tags
QFUScoreConfig = get_scoring_config
QFUTagsConfig = get_tags_config
QFUClientConfig = get_clients_config
QFUClientList = get_clients_list

__all__ = [
    "QFUTrackerConfig",
    "QFUTrackerList",
    "QFUScoreConfig",
    "QFUTagsConfig",
    "QFUClientConfig",
    "QFUClientList",
]
