"""Checker for torrent trackers."""
from qbittorrentapi import TorrentDictionary

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import APITorrentInfos

config = get_config()


def _process_tracker_check(
    torrent: APITorrentInfos,
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
            if keyword in torrent.tracker:
                logger.debug(
                    f"Torrent {torrent.name}:{torrent.hash_v1} is from tracker {tag}",
                )
                return tag
    else:
        logger.debug(f"Torrent {torrent.name}:{torrent.hash_v1} as no configured tracker")
        return config.tags.unknown_tracker_tag


def get_torrent_tracker(torrent: APITorrentInfos) -> str:
    """Get torrent tracker.
    :param torrent: Torrent to get tracker from
    :type torrent: TorrentInfos
    :return: Tracker tag
    :rtype: str"""
    return _process_tracker_check(torrent=torrent)


def _process_issue_tracker_check(
    torrent: TorrentDictionary,
) -> bool:
    for tracker in torrent.trackers:
        if tracker.status == 4:
            logger.debug(f"Tracker issue: {tracker.url} for {torrent.name}, {torrent.hash}")
            return True
    else:
        logger.debug(f"No tracker issue for {torrent.name}, {torrent.hash}")
        return False


def check_issue_tracker(torrent: TorrentDictionary) -> bool:
    """Get torrent tracker.
    :param torrent: Torrent to get tracker from
    :type torrent: TorrentInfos
    :return: True if issue, False otherwise
    :rtype: bool"""
    return _process_issue_tracker_check(torrent=torrent)
