"""init schemas"""
from .clients import ClientConfig, ClientsConfig
from .scoring import ScoringConfig
from .tags import TagsConfig
from .torrents import APITorrentInfos, TorrentInfos
from .trackers import TrackerConfig, TrackersConfig

__all__ = [
    "ClientConfig",
    "ScoringConfig",
    "TagsConfig",
    "TrackerConfig",
    "APITorrentInfos",
    "TorrentInfos",
    "TrackersConfig",
    "ClientsConfig",
]
