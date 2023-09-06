"""Check if torrent is cross-seeded."""

from typing import Tuple

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import APITorrentInfos

config = get_config()


# ! Containe fix for cross-seed issues with qBittorrent that re-download data
def _process_cross_seed_check(
    torrent: APITorrentInfos,
    config: Config = config,
) -> bool | Tuple[str, str]:
    """Process cross seed check.
    :param torrent: Torrent to check
    :type torrent: TorrentInfos
    :param config: Config, defaults to config
    :type config: Config, optional
    :return: False if not cross-seeded, bool
             content_path, hash if cross-seeded and not downloaded, Tuple[str, str]
    :rtype: bool | Tuple[str, str]
    """
    if torrent.downloaded == 0 and config.tags.cross_seed_tag in torrent.tags:
        logger.debug(f"Torrent {torrent.name} is cross-seeded")
        return (torrent.content_path, torrent.hash_v1)
    elif torrent.downloaded > 0 and config.tags.cross_seed_tag in torrent.tags:
        logger.debug(f"Torrent {torrent.name} is cross-seeded but has downloaded data")
        return False
    else:
        logger.debug(f"Torrent {torrent.name} is not cross-seeded")
        return False


def check_torrent_cross_seed(torrent: APITorrentInfos) -> bool | Tuple[str, str]:
    """Check if torrent are a cross seed.
    :param torrent: Torrent to check
    :type torrent: TorrentInfos
    :return: False if not cross-seeded, bool
             content_path, hash if cross-seeded and not downloaded, Tuple[str, str]
    :rtype: bool | Tuple[bool, str, str]"""
    return _process_cross_seed_check(torrent=torrent)
