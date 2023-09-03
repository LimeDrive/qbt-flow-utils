"""Scoring functions for torrents."""

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import APITorrentInfos

config = get_config()


def _process_torrent_scoring(
    torrent: APITorrentInfos,
    config: Config = config,
) -> float:
    """Process torrent scoring."""
    coef = config.scoring.score_calculation
    tags = torrent.tags  # TODO: check if tags is a list in schema with validator

    score = 10

    for tag in tags:
        if tag in config.tags_extra_scrore_dict:
            score += config.tags_extra_scrore_dict[tag]

    score += torrent.ratio * coef.coef_seed_ratio
    score += torrent.num_complete * coef.coef_nums_seeder
    score += (torrent.seeding_time / 60 / 60 / 24) * coef.coef_day_seed_time
    score = round(score, 2)

    logger.debug(f"Score for {torrent.name} is {score}")
    return score


def get_torrent_score(torrent: APITorrentInfos) -> float:
    """Get torrent score.
    :param torrent: torrent to get score
    :type torrent: APITorrentInfos
    :return: torrent score
    :rtype: float"""
    return _process_torrent_scoring(torrent=torrent)