"""Base module for torrents infos list."""

from typing import Dict

import qbittorrentapi as qbt
from pydantic import ValidationError

from ..checkers import (
    check_issue_tracker,
    check_public_tracker,
    check_torrent_cross_seed,
    check_torrent_hard_links,
    check_torrent_hit_and_run,
    get_torrent_tracker,
)
from ..config import Config, get_config
from ..logging import logger
from ..schemas.torrents import APITorrentInfos, TorrentInfos
from ..scoring import get_torrent_score

config = get_config()


def _process_torrents_infos_list(
    torrents: qbt.TorrentInfoList,
    client_name: str = "local",
    config: Config = config,
) -> Dict[str, TorrentInfos]:
    """Process torrents infos list.
    :param torrents: Torrents list
    :type torrents: qbt.TorrentInfoList
    :param client_name: Client name, defaults to "local"
    :type client_name: str, optional
    :param config: Config, defaults to config
    :type config: Config, optional
    :return: Torrents infos list
    :rtype: Dict[str, TorrentInfos]
    :raises AssertionError: torrents_list is empty
    :raises ValidationError: Could not validate torrent from api data
    """
    torrents_list: Dict[str, TorrentInfos] = {}

    for torrent in torrents:
        try:
            api_torrent_infos = APITorrentInfos.model_validate(torrent)
        except ValidationError as e:
            logger.error(f"Could not validate torrent from api data {torrent.hash}: {e}")
            continue

        if api_torrent_infos:
            torrent_info = TorrentInfos(api=api_torrent_infos, client=client_name)
            tracker_tag = get_torrent_tracker(torrent=api_torrent_infos)
            torrent_info.tracker_tag = tracker_tag

            torrent_info.score = get_torrent_score(
                torrent=api_torrent_infos,
                tracker_tag=tracker_tag,
            )

            if config.tags.auto_tags_hit_and_run:
                torrent_info.is_hit_and_run = check_torrent_hit_and_run(
                    torrent=api_torrent_infos,
                    tracker_tag=tracker_tag,
                )

            if client_name == "local" and config.settings.check_hard_links:
                torrent_info.is_hard_link = check_torrent_hard_links(
                    torrent=api_torrent_infos,
                    client=client_name,
                )

            if config.settings.check_cross_seed:
                torrent_info.is_cross_seed = check_torrent_cross_seed(torrent=api_torrent_infos)

            if config.tags.auto_tags_public:
                torrent_info.is_public = check_public_tracker(torrent=api_torrent_infos)

            if config.tags.auto_tags_tracker_issue:
                torrent_info.is_issue = check_issue_tracker(torrent=torrent)

            if torrent.state in ["forcedUP", "stalledDL", "queuedUP", "pausedUP", "uploading"]:
                torrents_list[str(torrent.hash)] = torrent_info

    assert torrents_list != {}, "torrents_list is empty"  # noqa: S101
    return torrents_list


def get_torrents_infos_list(
    torrents: qbt.TorrentInfoList,
    client_name: str = "local",
    config: Config = config,
) -> Dict[str, TorrentInfos]:
    """Get torrents infos list.

    :param torrents: Torrents list
    :type torrents: `TorrentInfoList`
    :param client_name: Client name, defaults to "local"
    :type client_name: str, optional
    :param config: Config, defaults to config
    :type config: Config, optional
    :return: Torrents infos list with torrent hash as key and TorrentInfos as value
    :rtype: `Dict[str, TorrentInfos]`

    1. `issue_tracker` : This function checks if there are any issues with the torrent's tracker.
    2. `public_tracker`: It determines whether the torrent is from a public tracker or not.
    3. `cross_seed`    : This check identifies if the torrent is a cross-seed, meaning it is
    available on multiple trackers.
    4. `hard_links`    : It checks if the torrent has hard links,vwhich are multiple references
    to the same file on the file system.
    5.  `hit_and_run`  : This check determines if the torrent is a hit-and-run, which refers to
    downloading a file and immediately stopping the seeding process.
    6. `tracker_tag`   : Is retrieved using the  `get_torrent_tracker` function and is assigned
    to the  tracker_tag attribute of the  TorrentInfos  object.
    7. `scoring`       : Is calculated using the  get_torrent_score  function, based on the torrent
    information and the tracker tag. The score is then assigned to the  score  attribute of the
    `TorrentInfos`  object.
    """
    return _process_torrents_infos_list(torrents=torrents, client_name=client_name, config=config)


if __name__ == "__main__":
    pass
    # from unittest.mock import MagicMock

    # import pytest

    # # Moke real data from client for pytest, when the testenv are ready

    # def test_process_torrents_infos_list_valid():
    #     """Test _process_torrents_infos_list() with valid torrent data."""
    #     client = MagicMock()
    #     client.torrents_info.return_value = [{}]  # Mock torrent data
    #     config = MagicMock()

    #     torrents_list = _process_torrents_infos_list(client, config=config)
    #     assert torrents_list != {}

    # def test_process_torrents_infos_list_invalid():
    #     """Test _process_torrents_infos_list() with invalid torrent data."""
    #     client = MagicMock()
    #     client.torrents_info.return_value = [{}]  # Mock invalid torrent data
    #     config = MagicMock()

    #     with pytest.raises(AssertionError):
    #         _process_torrents_infos_list(client, config=config)
