"""Connection to qBittorrent client."""
from typing import Dict

import qbittorrentapi as qbt

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas.torrents import APITorrentInfos


class QBTSession:
    """Creates qBittorrent client session."""

    def __init__(self, client_name: str, config: Config) -> None:
        """Initialize qBittorrent client connection."""
        self.client_name = client_name
        self.config = config
        self.client = qbt.Client(
            **self.config.clients[client_name].login.model_dump(exclude_none=True)
        )
        try:
            self.client.auth_log_in()
            logger.info(f"Connected to qBittorrent client {self.client.app.version}")
        except (
            qbt.APIConnectionError,
            qbt.LoginFailed,
            qbt.UnsupportedQbittorrentVersion,
            qbt.Forbidden403Error,
        ) as e:
            logger.error(f"Could not connect to qBittorrent {client_name} client: {e}")
            raise

        self.torrents_info = self.get_client_torrents_info()

    def get_session(self) -> qbt.Client:
        """Gets qBittorrent client session."""
        return self.client

    def toggle_alt_speed_limits(self, toggle: bool, up_kibs: int, down_kibs: int) -> None:
        """Set alternative speed limits or toggle it.
        :param toggle: True to enable, False to disable
        :param up_kibs: Upload speed limit in KiB/s (0 for unlimited)
        :param down_kibs: Download speed limit in KiB/s (0 for unlimited)
        :return: None
        """
        try:
            if toggle:
                if self.client.application.preferences.alt_dl_limit != str(
                    down_kibs,
                ) or self.client.application.preferences.alt_up_limit != str(up_kibs):
                    self.client.application.preferences = {
                        "alt_dl_limit": str(down_kibs),
                        "alt_up_limit": str(up_kibs),
                    }
                    logger.info(
                        f"Alternative speed limits set to {up_kibs} KiB/s up and"
                        f" {down_kibs} KiB/s down.",
                    )
                self.client.transfer_setSpeedLimitsMode(True)
                logger.info("Alternative speed limits enabled.")
            else:
                self.client.transfer_setSpeedLimitsMode(False)
                logger.info("Alternative speed limits disabled.")
        except:
            logger.error("Could not set alternative speed limits.")
            raise

    def get_client_torrents_info(self) -> qbt.TorrentInfoList:
        """Get torrents list from client."""
        return self.client.torrents_info(status_filter="all", sort="added_on")

    def api_torrents_dict(self) -> Dict[str, APITorrentInfos]:
        """Create qfu api base torrents dict.
        To be used as base for qfu torrents list.
        :return: Dict of torrents with hash as key and `APITorrentInfos` as value
        :rtype: `Dict[str, APITorrentInfos]`

        :Examples return:
        >>> {"hash1": APITorrentInfos, "hash2": APITorrentInfos}
        """
        torrents_list = {}
        for torrent in self.torrents_info:
            torrents_list[torrent.hash] = APITorrentInfos.model_validate(torrent)
        return torrents_list


if __name__ == "__main__":
    config = get_config()

    if "local" in config.clients_list:
        local_client = QBTSession("local", config=config)
