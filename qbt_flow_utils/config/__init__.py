"""Configuration files for qbt_flow_utils."""
from typing import Dict, List

from pydantic import BaseModel, ValidationError

from qbt_flow_utils.config.config import (
    get_clients_config,
    get_clients_list,
    get_scoring_config,
    get_tags_config,
    get_tags_extra_scrore_dict,
    get_trackers_config,
    get_trackers_tags_list,
)
from qbt_flow_utils.config.settings import Settings, settings
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import ClientsConfig, ScoringConfig, TagsConfig, TrackersConfig


class Config(BaseModel):
    """Configuration object for qbt_flow_utils.
    `clients`: Clients config
        :type clients: `ClientsConfig`
    `clients_list`: Clients list
        :type clients_list: `List[str]`
    `scoring`: Scoring config
        :type scoring: `ScoringConfig`
    `tags`: Tags config
        :type tags: `TagsConfig`
    `tags_extra_scrore_dict`: Tags extra score dict
        :type tags_extra_scrore_dict: `Dict[str, int]`
    `trackers`: Trackers config
        :type trackers: `TrackersConfig`
    `trackers_tags_list`: Trackers tags list
        :type trackers_tags_list: `List[str]`
    `settings`: Settings
        :type settings: `Settings`
    """

    clients: ClientsConfig
    clients_list: List[str]
    scoring: ScoringConfig
    tags: TagsConfig
    tags_extra_scrore_dict: Dict[str, int]
    trackers: TrackersConfig
    trackers_tags_list: List[str]
    settings: Settings


def _config() -> Config:
    """Get configuration object for qbt_flow_utils.
    :return: Configuration object for qbt_flow_utils.
    :rtype: Config"""
    try:
        config = Config(
            clients=get_clients_config(),
            clients_list=get_clients_list(),
            scoring=get_scoring_config(),
            tags=get_tags_config(),
            tags_extra_scrore_dict=get_tags_extra_scrore_dict(),
            trackers=get_trackers_config(),
            trackers_tags_list=get_trackers_tags_list(),
            settings=settings,
        )
    except ValidationError as e:
        logger.error("Error loading config file. : %s", e)
        raise
    else:
        return config


config = _config()


def get_config() -> Config:
    """Get configuration object for qbt_flow_utils.
    :return: Configuration object for qbt_flow_utils.
    :rtype: Config"""
    return config


__all__ = [
    "Config",
    "get_config",
]
