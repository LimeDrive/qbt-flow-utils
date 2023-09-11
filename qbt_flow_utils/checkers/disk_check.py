"""Functions for checking disk space."""
import qbittorrentapi as qbt
from pydantic import BaseModel, ByteSize

from ..config import Config, get_config, logger

config: Config = get_config()
logger = logger


class DiskUsage(BaseModel):
    """Disk usage information."""

    total: ByteSize = ByteSize(0)
    used: ByteSize = ByteSize(0)
    free: ByteSize
    percent: float = 0


class DiskUsageToFree(DiskUsage):
    """Disk space to free."""

    to_free: ByteSize


def _get_local_disk_usage(path: str) -> DiskUsage:
    """Get disk usage information for a given path.
    :param path: Path to check disk usage for.
    :type path: str
    :return: Disk usage information.
    :rtype: DiskUsage
    """
    try:
        import shutil

        total, used, free = shutil.disk_usage(path)
        return DiskUsage(
            total=ByteSize(total),
            used=ByteSize(used),
            free=ByteSize(free),
            percent=round(used / total * 100, 2),
        )
    except Exception:
        logger.exception(f"Could not get disk usage for {path}")
        raise


def _get_api_free_space_on_disk(
    client_maindata: qbt.SyncMainDataDictionary,
) -> DiskUsage:
    return DiskUsage(free=ByteSize(client_maindata.server_state.free_space_on_disk))  # type: ignore


def _process_client_disk_control(
    client_name: str,
    client_maindata: qbt.SyncMainDataDictionary,
    config: Config = config,
) -> None | DiskUsageToFree:
    """Process client disk control.
    :param client_name: Client name.
    :type client_name: str
    :param client_maindata: Client maindata.
    :type client_maindata: qbt.SyncMainDataDictionary
    :param config: Config.
    :type config: Config
    :return: Disk usage information or None if no disk space needs to be freed.
    """
    try:
        client_config = config.clients[client_name].disk_control_method.model_dump(
            exclude_none=True,
        )
        if "max_percents" and "path_to_check" in client_config:
            disk = _get_local_disk_usage(client_config["path_to_check"])
            if disk.percent >= client_config["max_percents"]:
                return DiskUsageToFree(
                    total=disk.total,
                    used=disk.used,
                    free=disk.free,
                    percent=disk.percent,
                    to_free=ByteSize(
                        disk.total - (disk.total * client_config["max_percents"] / 100),
                    ),
                )
            else:
                return None
        elif "keep_free_gib" in client_config:
            free_disk = _get_api_free_space_on_disk(client_maindata)
            if free_disk.free <= client_config["keep_free_gib"]:
                return DiskUsageToFree(
                    free=free_disk.free,
                    to_free=ByteSize(client_config["keep_free_gib"] - free_disk.free),
                )
            else:
                return None
        else:
            logger.error(
                f"Could not process disk control for {client_name}"
                " because of missing config values.",
            )
    except ValueError:
        logger.exception(f"Could not process disk control for {client_name}")
        raise


def control_disk_check(
    client_name: str,
    client_maindata: qbt.SyncMainDataDictionary,
) -> None | DiskUsageToFree:
    """Process disk control.
    :param client_name: Client name.
    :type client_name: str
    :param client_maindata: Client maindata.
    :type client_maindata: qbt.SyncMainDataDictionary
    :return: Disk usage information.
    :rtype: DiskUsageToFree or None if no disk space needs to be freed."""
    return _process_client_disk_control(client_name=client_name, client_maindata=client_maindata)
