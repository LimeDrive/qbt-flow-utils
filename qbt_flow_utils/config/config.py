"""Config main validation module."""
import os
from typing import List, Tuple

import yaml
from box import Box
from pydantic import ValidationError

from ..logging import logger
from ..schemas import ClientConfig, ScoringConfig, TagsConfig, TrackerConfig
from ..settings import settings


def _load_trackers_config(config_path: str) -> Tuple[Box, List[str]]:
    """Load trackers config.

    :param config_path: Path to trackers config directory.
    :type config_path: str
    :return: Tuple of trackers config and list of trackers tags.
    :rtype: Tuple[Box, List[str]]
    :raises ValidationError: If tracker config is invalid.
    :raises FileNotFoundError: If config directory does not exist.
    :raises ValueError: If no .yml or .yaml files found in config directory.
    """
    if not os.path.isdir(config_path):
        logger.info(f"Directory '{config_path}' does not exist.")
        raise FileNotFoundError(f"Directory '{config_path}' does not exist.")

    trackers_config = {}
    trackers_tags = []

    files = [f for f in os.listdir(config_path) if f.endswith((".yml", ".yaml"))]
    if not files:
        logger.info(f"No .yml or .yaml files found in '{config_path}' directory.")
        raise ValueError(f"No .yml or .yaml files found in '{config_path}' directory.")

    for filename in files:
        if filename.endswith((".yml", ".yaml")):
            with open(os.path.join(config_path, filename)) as file:
                data = yaml.safe_load(file)
            try:
                tracker_config = TrackerConfig.model_validate(data)
                tracker_tag = tracker_config.tracker_tag
                trackers_tags.append(tracker_tag)
                tracker_config_dict = tracker_config.model_dump(exclude_none=True)
                trackers_config[tracker_tag] = tracker_config_dict
            except ValidationError:
                logger.info(f"Invalid tracker config file {filename}")
                raise

    return Box(trackers_config, frozen_box=True), trackers_tags


def _load_scoring_config(config_file: str) -> Box:
    """Load scoring config.

    :param config_file: Path to scoring config file.
    :type config_file: str
    :return: Scoring config.
    :rtype: Box
    :raises ValidationError: If scoring config is invalid.
    :raises FileNotFoundError: If config file does not exist.
    """
    if not os.path.isfile(config_file):
        logger.info(f"File '{config_file}' does not exist.")
        raise FileNotFoundError(f"File '{config_file}' does not exist.")

    with open(config_file) as file:
        data = yaml.safe_load(file)

    try:
        scoring_config = ScoringConfig.model_validate(data)
        scoring_config_dict = scoring_config.model_dump(exclude_none=True)
    except ValidationError:
        logger.info(f"Invalid scoring config file {config_file}")
        raise

    return Box(scoring_config_dict, frozen_box=True)


def _load_tags_config(config_file: str) -> Box:
    """Load tags config.

    :param config_file: Path to tags config file.
    :type config_file: str
    :return: Tags config.
    :rtype: Box
    :raises ValidationError: If tags config is invalid.
    :raises FileNotFoundError: If config file does not exist.
    """
    if not os.path.isfile(config_file):
        logger.info(f"File '{config_file}' does not exist.")
        raise FileNotFoundError(f"File '{config_file}' does not exist.")

    with open(config_file) as file:
        data = yaml.safe_load(file)

    try:
        tags_config = TagsConfig.model_validate(data)
        tags_config_dict = tags_config.model_dump(exclude_none=True)
    except ValidationError:
        logger.info(f"Invalid tags config file {config_file}")
        raise

    return Box(tags_config_dict, frozen_box=True)


def _load_clients_config(config_dir: str) -> Tuple[Box, List[str]]:
    """Load clients config.

    :param config_dir: Path to clients config directory.
    :type config_dir: str
    :return: Tuple of clients config and list of clients names.
    :rtype: Tuple[Box, List[str]]
    :raises ValidationError: If clients config is invalid.
    :raises FileNotFoundError: If config directory does not exist.
    :raises ValueError: If no .yml or .yaml files found in config directory.
    """
    if not os.path.isdir(config_dir):
        logger.info(f"Directory '{config_dir}' does not exist.")
        raise FileNotFoundError(f"Directory '{config_dir}' does not exist.")

    clients_config = {}
    clients_list = []

    files = [f for f in os.listdir(config_dir) if f.endswith((".yml", ".yaml"))]
    if not files:
        logger.info(f"No .yml or .yaml files found in '{config_dir}' directory.")
        raise ValueError(f"No .yml or .yaml files found in '{config_dir}' directory.")

    for filename in files:
        if filename.endswith((".yml", ".yaml")):
            with open(os.path.join(config_dir, filename)) as file:
                data = yaml.safe_load(file)
            try:
                client_config = ClientConfig.model_validate(data)
                client_name = filename.split("_")[0]
                clients_list.append(client_name)
                client_config_dict = client_config.model_dump(exclude_none=True)
                clients_config[client_name] = client_config_dict
            except ValidationError:
                logger.info(f"Invalid client config file {filename}")
                raise

    return Box(clients_config, frozen_box=True), clients_list


config_folder = settings.config_folder
trackers_config_folder = os.path.join(config_folder, "trackers_config")
clients_config_folder = os.path.join(config_folder, "clients_config")
scoring_config_file = os.path.join(config_folder, "scoring_config.yml")
tags_config_file = os.path.join(config_folder, "tags_config.yml")

trackers_config, trackers_tags = _load_trackers_config(trackers_config_folder)
clients_config, clients_list = _load_clients_config(clients_config_folder)
scoring_config = _load_scoring_config(scoring_config_file)
tags_config = _load_tags_config(tags_config_file)


def get_trackers_config() -> Box:
    return trackers_config


def get_trackers_tags() -> List[str]:
    return trackers_tags


def get_scoring_config() -> Box:
    return scoring_config


def get_tags_config() -> Box:
    return tags_config


def get_clients_config() -> Box:
    return clients_config


def get_clients_list() -> List[str]:
    return clients_list
