"""Functions for tagging torrents."""

from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Tuple

from ..config import Config, get_config
from ..logging import logger
from ..schemas.torrents import TorrentInfos

config = get_config()


def _handle_tag(
    tag: str,
    condition: bool | None,
    torrent_tags: List[str],
    add_tags: List[str],
    remove_tags: List[str],
    auto_tag: bool,
) -> None:
    """Handle a tag based on the condition and auto_tag."""
    if auto_tag and condition is not None:
        if condition and tag not in torrent_tags:
            add_tags.append(tag)
        elif not condition and tag in torrent_tags:
            remove_tags.append(tag)


def _process_torrents_tags(
    torrents: Dict[str, TorrentInfos],
    config: Config = config,
) -> Tuple[Optional[DefaultDict[str, List[str]]], Optional[DefaultDict[str, List[str]]]]:
    """Process torrents and generate tags to add and remove.
    :param torrents: Dict of torrents with infohash as key and TorrentInfos as value.
    :param config: Config object with rules for tagging.
    :return: A tuple of two dicts:
    :return: - tags_to_add: Dict with tag as key and list of infohashes as value.
    :return: - tags_to_remove: Dict with tag as key and list of infohashes as value.
    :return: If no tags to add or remove, the respective dict will be None.

    For each torrent, determine which tags should be added and removed based
    on the config rules.
    """
    logger.info("Processing torrents trackers tag")
    torrents_tags_to_add_dict: DefaultDict[str, List[str]] | None = defaultdict(list)
    torrents_tags_to_remove_dict: DefaultDict[str, List[str]] | None = defaultdict(list)

    for infohash, torrent in torrents.items():
        torrent_tags_to_add: List[str] = []
        torrent_tags_to_remove: List[str] = []

        tags = [
            (config.tags.tracker_issue_tag, torrent.is_issue, config.tags.auto_tags_tracker_issue),
            (config.tags.public_tag, torrent.is_public, config.tags.auto_tags_public),
            (
                config.tags.hit_and_run_tag,
                torrent.is_hit_and_run,
                config.tags.auto_tags_hit_and_run,
            ),
            (
                config.tags.no_hard_link_tag,
                not torrent.is_hard_link,
                config.tags.auto_tags_no_hard_link,
            ),
            (
                config.tags.download_limit_tag,
                torrent.is_down_limit,
                config.tags.auto_tags_download_limit,
            ),
            (config.tags.upload_limit_tag, torrent.is_up_limit, config.tags.auto_tags_upload_limit),
        ]

        for tag, condition, auto_tag in tags:
            _handle_tag(
                tag,
                condition,
                torrent.api.tags,
                torrent_tags_to_add,
                torrent_tags_to_remove,
                auto_tag,
            )

        if config.tags.auto_tags_trackers and torrent.tracker_tag is not None:
            if torrent.tracker_tag not in torrent.api.tags:
                torrent_tags_to_add.append(torrent.tracker_tag)
            if (
                config.tags.unknown_tracker_tag in torrent.api.tags
                and torrent.tracker_tag != config.tags.unknown_tracker_tag
            ):
                torrent_tags_to_remove.append(config.tags.unknown_tracker_tag)

        for tag in torrent_tags_to_add:
            torrents_tags_to_add_dict[tag].append(infohash)
        for tag in torrent_tags_to_remove:
            torrents_tags_to_remove_dict[tag].append(infohash)

    if not torrents_tags_to_add_dict:
        torrents_tags_to_add_dict = None

    if not torrents_tags_to_remove_dict:
        torrents_tags_to_remove_dict = None

    return torrents_tags_to_add_dict, torrents_tags_to_remove_dict


def get_torrents_tags_dicts(
    torrents: Dict[str, TorrentInfos],
) -> Tuple[Optional[DefaultDict[str, List[str]]], Optional[DefaultDict[str, List[str]]]]:
    """Get tags to add and remove from torrents.
    :param torrents: Dict of torrents with infohash as key and TorrentInfos as value.
    :return: A tuple of two dicts:
    :return: - tags_to_add: Dict with tag as key and list of infohashes as value.
    :return: - tags_to_remove: Dict with tag as key and list of infohashes as value.
    :return: If no tags to add or remove, the respective dict will be None.
    """
    return _process_torrents_tags(torrents=torrents)
