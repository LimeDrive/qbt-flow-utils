"""Checkers for Upload/Download limits."""

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.schemas import APITorrentInfos

config = get_config()


def _process_upload_limit_check(
    torrent: APITorrentInfos,
    config: Config = config,
) -> bool:
    """Check torrent upload limit."""
    return torrent.up_limit != 0


def _process_download_limit_check(
    torrent: APITorrentInfos,
    config: Config = config,
) -> bool:
    """Check torrent download limit."""
    return torrent.dl_limit != 0


def check_torrent_upload_limit(torrent: APITorrentInfos) -> bool:
    """Check if torrent has upload limit.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :return: True if torrent has upload limit, False otherwise
    :rtype: bool"""
    return _process_upload_limit_check(torrent=torrent)


def check_torrent_download_limit(torrent: APITorrentInfos) -> bool:
    """Check if torrent has download limit.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :return: True if torrent has download limit, False otherwise
    :rtype: bool"""
    return _process_download_limit_check(torrent=torrent)
