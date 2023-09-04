"""Functions for handling hit and run torrents."""

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import TorrentInfos

config = get_config()


def _process_hit_and_run_check(
    torrent: TorrentInfos,
    config: Config = config,
) -> bool:
    """Process hit and run check.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :param trackers_config: Trackers config, defaults to trackers_config
    :type trackers_config: TrackersConfig, optional
    :param trackers_tags: Trackers tags, defaults to trackers_tags
    :type trackers_tags: List[str], optional
    :return: True if hit and run, False otherwise
    :rtype: bool
    """
    for tag in config.trackers_tags_list:
        if tag in torrent.api.tags:
            hit_and_run_conditions = config.trackers[tag].hit_and_run.model_dump()
            # TODO: check timedelta objects in dump dict. and review the loop.
            for condition, threshold in hit_and_run_conditions.items():
                if condition == "ignore_hit_and_run" and threshold:
                    logger.debug(f"Hit and run check ignored for {tag}: {torrent.api.name}")
                    break
                elif (condition == "min_seed_time" and (torrent.api.seeding_time <= threshold)) or (
                    condition == "min_ratio" and (torrent.api.ratio >= threshold)
                ):
                    logger.debug(
                        f"Hit and run condition met for {tag}: {torrent.api.name},"
                        f" {torrent.api.hash_v1}",
                    )
                    return True
            else:
                logger.debug(
                    f"Hit and run condition not met for {tag}: {torrent.api.name},"
                    f" {torrent.api.hash_v1}",
                )
                return False
    else:
        logger.debug(f"Torrent {torrent.api.name} is not from a tracker in trackers_tags")
        return False


def check_torrent_hit_and_run(torrent: TorrentInfos) -> bool:
    """Check if torrent is hit and run.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :return: True if hit and run, False otherwise
    :rtype: bool"""
    return _process_hit_and_run_check(torrent=torrent)
