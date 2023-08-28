# tests/test_client_config.py
import pytest
from pydantic import ValidationError

from qbt_flow_utils.config.schemas.clients import ClientConfig


def test_valid_client_config():
    valid_config = {
        "login": {
            "host": "qbittorrent:8080",
            "port": 8080,
            "username": "admin",
            "password": "adminadmin",
        },
        "disk_control_method": {
            "max_percents": 15,
            "path_to_check": "/downloads",
        },
        "category": {
            "films-radarr": "/qBittorrent/films-radarr",
            "tv-sonarr": "/qBittorrent/tv-sonarr",
        },
        "path": {
            "downloads_path": "/qBittorrent",
            "recycle_bin": "/qBittorrent/.RecycleBin",
        },
    }
    ClientConfig.model_validate(valid_config)


def test_invalid_client_config():
    invalid_config = {
        "login": {
            "host": "qbittorrent:8080",
            "port": 8080,
            "username": "admin",
        },
        "disk_control_method": {
            "max_percents": 15,
            "path_to_check": "/downloads",
            "keep_free_gib": 10,  # This is invalid
        },
        "category": {
            "films-radarr": "/qBittorrent/films-radarr",
            "tv-sonarr": "/qBittorrent/tv-sonarr",
        },
        "path": {
            "downloads_path": "/qBittorrent",
            "recycle_bin": "/qBittorrent/.RecycleBin",
        },
    }
    with pytest.raises(ValidationError):
        ClientConfig.model_validate(invalid_config)
