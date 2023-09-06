"""Base List."""

from typing import Dict

from pydantic import ValidationError
from qbittorrentapi import TorrentInfoList

from qbt_flow_utils.config import Config, get_config
from qbt_flow_utils.flow_utils.checkers import (
    check_public_tracker,
    check_torrent_cross_seed,
    check_torrent_hard_links,
    check_torrent_hit_and_run,
    get_torrent_tracker,
)
from qbt_flow_utils.flow_utils.scoring import get_torrent_score
from qbt_flow_utils.logging import logger
from qbt_flow_utils.schemas.torrents import APITorrentInfos, TorrentInfos

config = get_config()


def _process_torrents_infos_list(
    torrents: TorrentInfoList,
    client: str = "local",
    config: Config = config,
) -> Dict[str, TorrentInfos]:
    """Process torrents infos list.
    :param torrents: Torrents to process
    :type torrents: TorrentInfoList
    :param client: Client name, defaults to "local"
    :type client: str, optional
    :param config: Config, defaults to config
    :type config: Config, optional
    :return: Torrents infos list
    :rtype: Dict[str, TorrentInfos]
    """
    torrents_list: Dict[str, TorrentInfos] = {}

    for torrent in torrents:
        api_torrent_infos = False

        try:
            # Validate the torrent data from the API
            api_torrent_infos = APITorrentInfos.model_validate(torrent)
        except ValidationError as e:
            # Log the error if validation fails
            logger.error(f"Could not validate torrent from api data {torrent.hash}: {e}")
            continue

        if api_torrent_infos:
            # Create a TorrentInfos object using the API data
            torrent_info = TorrentInfos(api=api_torrent_infos, client=client)

            # Get the tracker tag for the torrent
            tracker_tag = get_torrent_tracker(torrent=api_torrent_infos)

            # Set the tracker tag and score for the torrent
            torrent_info.tracker_tag = tracker_tag
            torrent_info.score = get_torrent_score(
                torrent=api_torrent_infos,
                tracker_tag=tracker_tag,
            )

            # Check if the torrent is a hit and run
            if config.tags.auto_tags_hit_and_run:
                torrent_info.is_hit_and_run = check_torrent_hit_and_run(
                    torrent=api_torrent_infos,
                    tracker_tag=tracker_tag,
                )

            # Check if the torrent has hard links
            if client == "local" and config.settings.check_hard_links:
                torrent_info.is_hard_link = check_torrent_hard_links(
                    torrent=api_torrent_infos,
                    client=client,
                )

            # Check if the torrent is a cross seed
            if config.settings.check_cross_seed:
                torrent_info.is_cross_seed = check_torrent_cross_seed(torrent=api_torrent_infos)

            # Check if the torrent is on a public tracker
            if config.tags.auto_tags_public:
                torrent_info.is_public = check_public_tracker(torrent=api_torrent_infos)

            # TODO: Check torrent is_issue

            # Add the torrent to the torrents_list dictionary
            # TODO: if statement for torrent_info.is_issue ans state.
            torrents_list[str(torrent.hash)] = torrent_info

    return torrents_list
