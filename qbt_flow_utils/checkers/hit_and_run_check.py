"""Functions for handling hit and run torrents."""

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.config.logging import logger
from qbt_flow_utils.schemas import APITorrentInfos

config = get_config()


def _process_hit_and_run_check(
    torrent: APITorrentInfos,
    tracker_tag: str,
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
    if not config.trackers[tracker_tag].hit_and_run.ignore_hit_and_run:
        hit_and_run_conditions = config.trackers[tracker_tag].hit_and_run.model_dump()
        for condition, threshold in hit_and_run_conditions.items():
            if (condition == "min_seed_time" and (torrent.seeding_time <= threshold)) or (
                condition == "min_ratio" and (torrent.ratio >= threshold)
            ):
                logger.debug(
                    f"Hit and run condition met for {tracker_tag}: {torrent.name}, {torrent.hash}",
                )
                return True
        else:
            logger.debug(
                f"Hit and run condition not met for {tracker_tag}: {torrent.name}, {torrent.hash}",
            )
            return False
    else:
        logger.debug(f"Hit and run ignored for {tracker_tag}: {torrent.name}, {torrent.hash}")
        return False


def check_torrent_hit_and_run(torrent: APITorrentInfos, tracker_tag: str) -> bool:
    """Check if torrent is hit and run.
    :param torrent: Torrent to check
    :type torrent: APITorrentInfos
    :return: True if hit and run, False otherwise
    :rtype: bool"""
    return _process_hit_and_run_check(torrent=torrent, tracker_tag=tracker_tag)
