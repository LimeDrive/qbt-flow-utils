"""Main entry point for the application."""
from qbt_flow_utils.config import configure_logging, get_config, logger
from qbt_flow_utils.qbittorrent import QBTSession
from qbt_flow_utils.schemas import APITorrentInfos

if __name__ == "__main__":
    configure_logging()
    config = get_config()
    logger.info("Starting qbt_flow_utils")
    logger.info(f"Config: {config}")

    if "local" in config.clients_list:
        local_client = QBTSession("local", config=config)
        torrents = local_client.get_client_torrents_info()
        for torrent in torrents:
            test = APITorrentInfos.model_validate(torrent)
            print(test)
