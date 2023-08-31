"""Connection to qBittorrent client."""
import qbittorrentapi as qbt
from box import Box

from qbt_flow_utils.config import get_clients_config, get_clients_list
from qbt_flow_utils.logging import logger


class QBTConnect:
    """Connection to qBittorrent client."""

    def __init__(self, client_name: str, config: Box) -> None:
        """Initialize qBittorrent client connection."""
        self.client_name = client_name
        self.config = config
        try:
            self.client = qbt.Client(**self.config[client_name].login)
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


if __name__ == "__main__":
    clients_config = get_clients_config()
    clients_list = get_clients_list()

    if "local" in clients_config:
        local_client = QBTConnect("local", clients_config)
