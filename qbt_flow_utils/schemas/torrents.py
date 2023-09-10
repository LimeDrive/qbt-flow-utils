"""Schema for torrent data from qBittorrent API."""
from datetime import datetime, timedelta
from typing import List, Tuple

from pydantic import BaseModel, ByteSize, ConfigDict, NegativeInt, field_validator

# * Add all fields from qbtittorrentapi.torrent.TorrentInfo,
# * for the moment they are only the ones come from the qbittorrent docapi


class APITorrentInfos(BaseModel):
    """Schema for torrent data from qBittorrent API."""

    model_config = ConfigDict(extra="allow")

    added_on: datetime  # Time (Unix Epoch) when the torrent was added to the client
    amount_left: ByteSize  # Amount of data left to download (bytes)
    auto_tmm: bool  # Whether this torrent is managed by Automatic Torrent Management
    availability: float  # Percentage of file pieces currently available
    category: str | None  # Category of the torrent
    completed: ByteSize  # Amount of transfer data completed (bytes)
    completion_on: datetime  # Time (Unix Epoch) when the torrent completed
    content_path: str  # Absolute path of torrent content (root path for multifile torrents)
    dl_limit: ByteSize  # Torrent download speed limit (bytes/s).
    dlspeed: ByteSize  # Torrent download speed (bytes/s)
    download_path: str | None  # Path where this torrent's data is stored
    downloaded: ByteSize  # Amount of data downloaded
    downloaded_session: ByteSize  # Amount of data downloaded this session
    eta: timedelta  # Torrent ETA (seconds) estimated time the AVAILABLE CONTENT will be completed
    f_l_piece_prio: bool  # True if first last piece are prioritized
    force_start: bool  # True if force start is enabled for this torrent
    hash: str  # noqa: A003 # Torrent hash
    infohash_v1: str | None  # Torrent hash (v1)
    infohash_v2: str | None  # Torrent hash (v2)
    last_activity: datetime  # Last time (Unix Epoch) when a chunk was downloaded/uploaded
    magnet_uri: str  # Magnet URI corresponding to this torrent
    max_ratio: int | float  # Maximum share ratio until torrent is stopped from seeding/uploading
    max_seeding_time: timedelta | NegativeInt  # Max seeding time (seconds) until torrent is stopped
    name: str  # Torrent name
    num_complete: int  # Number of seeds in the swarm
    num_incomplete: int  # Number of leechers in the swarm
    num_leechs: int  # Number of leechers connected to
    num_seeds: int  # Number of seeds connected to
    priority: int  # Torrent priority.
    progress: float  # Torrent progress (percentage/100)
    ratio: int | float  # Torrent share ratio. Max ratio value: 9999.
    ratio_limit: ByteSize | NegativeInt  # Max share ratio until torrent is stopped from seeding
    save_path: str  # Path where this torrent's data is stored
    seeding_time: timedelta  # Torrent elapsed time while complete (seconds)
    seeding_time_limit: timedelta | NegativeInt  # Max seeding time (s) until torrent is stopped
    seen_complete: datetime  # Time (Unix Epoch) when this torrent was last seen complete
    seq_dl: bool  # True if sequential download is enabled
    size: ByteSize  # Total size (bytes) of files selected for download
    state: str  # Torrent state.
    super_seeding: bool  # True if super seeding is enabled
    tags: List[str] | None  # Comma-concatenated tag list of the torrent
    time_active: timedelta  # Total active time (seconds)
    total_size: ByteSize  # Total size (bytes) of all files (including unselected ones)
    tracker: str  # The first tracker. Returns empty string if no tracker is work.
    trackers_count: int  # Number of trackers
    up_limit: ByteSize  # Torrent upload speed limit (bytes/s).
    uploaded: ByteSize  # Amount of data uploaded
    uploaded_session: ByteSize  # Amount of data uploaded this session
    upspeed: ByteSize  # Torrent upload speed (bytes/s)

    @field_validator("tags", mode="before")
    def _process_tags(cls, value):
        if value == "":
            return None
        elif value != [""]:
            lst = [s.strip() for s in value.split(",")]
            return lst
        return value

    @field_validator("category", "download_path", "infohash_v1", "infohash_v2", mode="before")
    def _process_none(cls, value):
        if value == "":
            return None
        return value


class TorrentInfos(BaseModel):
    """Torrent infos."""

    api: APITorrentInfos
    client: str
    ok_removal: bool | None = None
    tracker_tag: str | None = None
    score: float | int | None = None
    is_hit_and_run: bool | None = None
    is_hard_link: bool | None = None
    is_public: bool | None = None
    is_issue: bool | None = None
    is_cross_seed: bool | Tuple[str, str] | None = None
    is_up_limit: bool | None = None
    is_down_limit: bool | None = None
