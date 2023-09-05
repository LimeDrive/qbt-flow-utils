"""Hardlink functions for torrents."""
import os

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import TorrentInfos

config = get_config()


def _process_hard_link_check(torrent: TorrentInfos, config: Config = config) -> bool:
    """Process hard link check."""
    content = torrent.api.content_path.replace(
        config.clients[torrent.client].path.downloads_path,
        config.settings.download_folder,
    )
    has_links = False

    def check_hard_links(directory: str) -> None:
        nonlocal has_links
        for root, _, files in os.walk(directory):
            if files:
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.stat(file_path).st_nlink > 1:
                        has_links = True
                        return

    if os.path.isdir(content):
        check_hard_links(content)
    else:
        has_links = os.stat(content).st_nlink > 1

    logger.debug(f"Torrent {torrent.api.name} hardlink check: {has_links}")
    return has_links


def check_torrent_hard_links(torrent: TorrentInfos) -> bool:
    """Check if torrent has hard links.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :return: True if torrent has hard links, False otherwise
    :rtype: bool"""
    return _process_hard_link_check(torrent=torrent)
