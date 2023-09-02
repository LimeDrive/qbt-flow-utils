"""Connection to qBittorrent client."""
import qbittorrentapi as qbt

from qbt_flow_utils.config import get_clients_config, get_clients_list
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import ClientsConfig


class QBTSession:
    """Creates qBittorrent client session."""

    def __init__(self, client_name: str, config: ClientsConfig) -> None:
        """Initialize qBittorrent client connection."""
        self.client_name = client_name
        self.config = config
        self.client = qbt.Client(**self.config[client_name].login.model_dump(exclude_none=True))
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

    def get_session(self) -> qbt.Client:
        """Gets qBittorrent client session."""
        return self.client


if __name__ == "__main__":
    clients_config = get_clients_config()
    clients_list = get_clients_list()

    if "local" in clients_list:
        local_client = QBTSession("local", clients_config)
