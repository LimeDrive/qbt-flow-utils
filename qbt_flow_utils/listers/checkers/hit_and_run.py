"""Functions for handling hit and run torrents."""
from typing import List

from qbt_flow_utils.config import get_trackers_config, get_trackers_tags_list
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import APITorrentInfos, TrackersConfig

trackers_config = get_trackers_config()
trackers_tags = get_trackers_tags_list()


def _process_hit_and_run_check(
    torrent: APITorrentInfos,
    trackers_config: TrackersConfig = trackers_config,
    trackers_tags: List[str] = trackers_tags,
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
    for tag in trackers_tags:
        if tag in torrent.tags:
            hit_and_run_conditions = trackers_config[tag].hit_and_run.model_dump(exclude_none=True)

            for condition, threshold in hit_and_run_conditions.items():
                if condition == "ignore_hit_and_run" and threshold:
                    logger.debug(f"Hit and run check ignored for {tag}: {torrent.name}")
                    break
                elif (
                    condition == "min_seed_time"
                    and (torrent.seeding_time <= (int(threshold) * 3600))
                ) or (condition == "min_ratio" and (torrent.ratio >= int(threshold))):
                    logger.debug(
                        f"Hit and run condition met for {tag}: {torrent.name}, {torrent.hash_v1}",
                    )
                    return True
            else:
                logger.debug(
                    f"Hit and run condition not met for {tag}: {torrent.name}, {torrent.hash_v1}",
                )
                return False
    else:
        logger.debug(f"Torrent {torrent.name} is not from a tracker in trackers_tags")
        return False


def check_torrent_hit_and_run(torrent: APITorrentInfos) -> bool:
    """Check if torrent is hit and run.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :return: True if hit and run, False otherwise
    :rtype: bool"""
    return _process_hit_and_run_check(torrent=torrent)
