"""Main entry point for the application."""
from qbt_flow_utils.config import configure_logging, get_config, logger
from qbt_flow_utils.qbittorrent import QBTSession


def main():
    configure_logging()
    config = get_config()
    logger.warning("dev print")
    logger.info(f"Config: {config}")

    if "local" in config.clients_list:
        QBTSession("local", config=config)


if __name__ == "__main__":
    main()
