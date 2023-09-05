"""Scoring functions for torrents."""

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import TorrentInfos

config = get_config()


def _process_torrent_scoring(
    torrent: TorrentInfos,
    config: Config = config,
) -> float:
    """Process torrent scoring."""
    coef = config.scoring.score_calculation
    tags = torrent.api.tags

    score = 10

    for tag in tags:
        if tag in config.tags_extra_scrore_dict:
            score += config.tags_extra_scrore_dict[tag]

    score += torrent.api.ratio * coef.coef_seed_ratio
    score += torrent.api.num_complete * coef.coef_nums_seeder
    score += (torrent.api.seeding_time.total_seconds() / 60 / 60 / 24) * coef.coef_day_seed_time
    score = round(score, 2)

    logger.debug(f"Score for {torrent.api.name} is {score}")
    return score


def get_torrent_score(torrent: TorrentInfos) -> float:
    """Get torrent score.
    :param torrent: torrent to get score
    :type torrent: APITorrentInfos
    :return: torrent score
    :rtype: float"""
    return _process_torrent_scoring(torrent=torrent)
