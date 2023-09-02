"""Actions Manager for qBittorrent"""
import qbittorrentapi as qbt

from qbt_flow_utils.logging import logger


class QBTUtils:
    """Utility class for qBittorrent actions."""

    def __init__(self, client: qbt.Client) -> None:
        """Initialize qBittorrent client actions."""
        self.client = client

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
                        f"Alternative speed limits set to {up_kibs} KiB/s up and {down_kibs} KiB/s"
                        " down.",
                    )
                self.client.transfer_setSpeedLimitsMode(True)
                logger.info("Alternative speed limits enabled.")
            else:
                self.client.transfer_setSpeedLimitsMode(False)
                logger.info("Alternative speed limits disabled.")
        except:
            logger.error("Could not set alternative speed limits.")
            raise
