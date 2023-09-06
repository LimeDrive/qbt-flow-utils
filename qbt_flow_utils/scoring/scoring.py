"""Scoring functions for torrents."""

from ..config import Config, get_config
from ..logging import logger
from ..schemas import APITorrentInfos

config = get_config()


def _process_torrent_scoring(
    torrent: APITorrentInfos,
    tracker_tag: str,
    config: Config = config,
) -> float:
    """Process torrent scoring."""
    coef = config.scoring.score_calculation

    score = 10
    score += torrent.ratio * coef.coef_seed_ratio
    score += torrent.num_complete * coef.coef_nums_seeder
    score += (torrent.seeding_time.total_seconds() / 60 / 60 / 24) * coef.coef_day_seed_time
    if tracker_tag in config.tags_extra_scrore_dict:
        score += config.tags_extra_scrore_dict[tracker_tag]

    score = round(score, 2)

    logger.debug(f"Score for {torrent.name} is {score}")
    return score


def get_torrent_score(torrent: APITorrentInfos, tracker_tag: str) -> float:
    """Get torrent score.
    :param torrent: torrent to get score
    :type torrent: APITorrentInfos
    :return: torrent score
    :rtype: float"""
    return _process_torrent_scoring(torrent=torrent, tracker_tag=tracker_tag)
