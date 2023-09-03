"""Hardlink functions for torrents."""
import os

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import APITorrentInfos

config = get_config()


def has_hard_links(path: str) -> bool:
    """Check if file has hard links.
    :param path: Path to file
    :type path: str
    :return: True if file has hard links, False otherwise
    :rtype: bool
    """
    return os.stat(path).st_nlink > 1


def _process_hard_link_check(
    torrent: APITorrentInfos,
    config: Config = config,
):
    root_path = config.settings.download_folder  # TODO: check path mapping with docker.
    torrent_path = torrent.content_path  # TODO: check if it will not be mor eff ti use filenames.

    if torrent_path.startswith("/"):  # check if path is absolute
        torrent_path = torrent_path.lstrip("/")  # remove leading slash

    content = os.path.join(root_path, torrent_path)

    if os.path.isdir(content):
        files = [os.path.join(content, filename) for filename in os.listdir(content)]
        has_links = any(has_hard_links(file) for file in files)
    else:
        has_links = has_hard_links(content)

    logger.debug(f"Torrent {torrent.name} hardlink check: {has_links}")
    return has_links


def check_torrent_hard_links(torrent: APITorrentInfos) -> bool:
    """Check if torrent has hard links.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :return: True if torrent has hard links, False otherwise
    :rtype: bool"""
    return _process_hard_link_check(torrent=torrent)
