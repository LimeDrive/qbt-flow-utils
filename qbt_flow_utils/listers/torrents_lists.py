"""Torrents lists utils."""
from typing import Dict

import qbittorrentapi as qbt

from qbt_flow_utils.schemas import APITorrentInfos


class TorrentsLists:
    """Torrents lists utils."""

    def __init__(self, client: qbt.Client) -> None:
        """Initialize torrents lists utils."""
        self.client = client
        self.qbt_torrents_list = self.get_client_torrents_list()

    def get_client_torrents_list(self) -> qbt.TorrentInfoList:
        """Get torrents list from client."""
        return self.client.torrents_info(status_filter="all", sort="added_on")

    def get_qfu_api_torrents_dict(self) -> Dict[str, APITorrentInfos]:
        """Create qfu api base torrents dict.
        To be used as base for qfu torrents list.
        :return: Dict of torrents with hash as key and APITorrentInfos as value
        :rtype: Dict[str, APITorrentInfos]
        """
        torrents_list = {}
        for torrent in self.qbt_torrents_list:
            torrents_list[torrent.hash] = APITorrentInfos.model_validate(torrent)
        return torrents_list
