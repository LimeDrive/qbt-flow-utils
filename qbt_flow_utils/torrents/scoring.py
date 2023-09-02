"""Scoring functions for torrents."""

from qbt_flow_utils.config import get_scoring_config, get_tags_extra_scrore_dict
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas import APITorrentInfos, ScoringConfig

scoring_config = get_scoring_config()
tags_extra_score = get_tags_extra_scrore_dict()


def _process_torrent_scoring(
    torrent: APITorrentInfos,
    scoring_config: ScoringConfig = scoring_config,
    tags_extra_score: dict = tags_extra_score,
) -> float:
    """Process torrent scoring."""
    coef = scoring_config.score_calculation
    tags = torrent.tags  # TODO: check if tags is a list in schema with validator

    score = 10

    for tag in tags:
        if tag in tags_extra_score:
            score += tags_extra_score[tag]

    score += torrent.ratio * coef.coef_seed_ratio
    score += torrent.num_complete * coef.coef_nums_seeder
    score += (torrent.seeding_time / 60 / 60 / 24) * coef.coef_day_seed_time
    score = round(score, 2)

    logger.debug(f"Score for {torrent.name} is {score}")
    return score


def get_torrent_score(torrent: APITorrentInfos) -> float:
    """Get torrent score."""
    return _process_torrent_scoring(torrent=torrent)
