"""init schemas"""
from qbt_flow_utils.schemas.clients import ClientConfig, ClientsConfig
from qbt_flow_utils.schemas.scoring import ScoringConfig
from qbt_flow_utils.schemas.tags import TagsConfig
from qbt_flow_utils.schemas.torrents import APITorrentInfos, QFUTorrentSettings, TorrentInfos
from qbt_flow_utils.schemas.trackers import TrackerConfig, TrackersConfig

__all__ = [
    "ClientConfig",
    "ScoringConfig",
    "TagsConfig",
    "TrackerConfig",
    "APITorrentInfos",
    "TorrentInfos",
    "QFUTorrentSettings",
    "TrackersConfig",
    "ClientsConfig",
]
