"""Checker for torrent trackers."""

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import TorrentInfos

config = get_config()


def _process_tracker_check(
    torrent: TorrentInfos,
    config: Config = config,
) -> str:
    """Process tracker check.
    :param torrent: Torrent to check
    :type torrent: TorrentInfos
    :param config: Config, defaults to config
    :type config: Config, optional
    :return: Tracker tag
    :rtype: str
    """
    for tag in config.trackers_tags_list:
        for keyword in config.trackers[tag].tracker_keywords:
            if keyword in torrent.api.tracker:
                logger.debug(
                    f"Torrent {torrent.api.name}:{torrent.api.hash_v1} is from tracker {tag}",
                )
                return tag
    else:
        logger.debug(f"Torrent {torrent.api.name}:{torrent.api.hash_v1} as no configured tracker")
        return config.tags.unknown_tracker_tag


def get_torrent_tracker(torrent: TorrentInfos) -> str:
    """Get torrent tracker.
    :param torrent: Torrent to get tracker from
    :type torrent: TorrentInfos
    :return: Tracker tag
    :rtype: str"""
    return _process_tracker_check(torrent=torrent)
