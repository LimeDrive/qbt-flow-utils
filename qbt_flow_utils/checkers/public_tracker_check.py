"""Checker for public torrent trackers."""

from qbt_flow_utils.schemas import APITorrentInfos


def check_public_tracker(
    torrent: APITorrentInfos,
) -> bool:
    """Process public tracker check.
    :param torrent: Torrent to check
    :type torrent: TorrentInfos
    :return: True if public, False otherwise
    :rtype: bool
    """
    return torrent.trackers_count > 1
