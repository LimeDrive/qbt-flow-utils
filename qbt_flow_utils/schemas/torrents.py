"""Schema for torrent data from qBittorrent API."""
from pydantic import BaseModel, ConfigDict


# TODO: Add all fields from qbtittorrentapi.torrent.TorrentInfo,
# TODO: for the moment they are only the ones come from the qbittorrent docapi
class APITorrentInfos(BaseModel):
    """Schema for torrent data from qBittorrent API."""

    model_config = ConfigDict(extra="allow")

    added_on: int  # Time (Unix Epoch) when the torrent was added to the client
    amount_left: int  # Amount of data left to download (bytes)
    auto_tmm: bool  # Whether this torrent is managed by Automatic Torrent Management
    availability: float  # Percentage of file pieces currently available
    category: str  # Category of the torrent
    completed: int  # Amount of transfer data completed (bytes)
    completion_on: int  # Time (Unix Epoch) when the torrent completed
    content_path: str  # Absolute path of torrent content (root path for multifile torrents,
    # absolute file path for singlefile torrents)
    dl_limit: int  # Torrent download speed limit (bytes/s). -1 if unlimited.
    dlspeed: int  # Torrent download speed (bytes/s)
    downloaded: int  # Amount of data downloaded
    downloaded_session: int  # Amount of data downloaded this session
    eta: int  # Torrent ETA (seconds)
    f_l_piece_prio: bool  # True if first last piece are prioritized
    force_start: bool  # True if force start is enabled for this torrent
    hash_v1: str  # TODO: Torrent hash (check with the real return value)
    last_activity: int  # Last time (Unix Epoch) when a chunk was downloaded/uploaded
    magnet_uri: str  # Magnet URI corresponding to this torrent
    max_ratio: float  # Maximum share ratio until torrent is stopped from seeding/uploading
    max_seeding_time: int  # Maximum seeding time (seconds) until torrent is stopped from seeding
    name: str  # Torrent name
    num_complete: int  # Number of seeds in the swarm
    num_incomplete: int  # Number of leechers in the swarm
    num_leechs: int  # Number of leechers connected to
    num_seeds: int  # Number of seeds connected to
    priority: int  # Torrent priority. Returns -1 if queuing is disabled or torrent is in seed mode
    progress: float  # Torrent progress (percentage/100)
    ratio: float  # Torrent share ratio. Max ratio value: 9999.
    ratio_limit: float  # TODO (what is different from max_ratio?)
    save_path: str  # Path where this torrent's data is stored
    seeding_time: int  # Torrent elapsed time while complete (seconds)
    seeding_time_limit: int  # TODO (what is different from max_seeding_time?)
    seen_complete: int  # Time (Unix Epoch) when this torrent was last seen complete
    seq_dl: bool  # True if sequential download is enabled
    size: int  # Total size (bytes) of files selected for download
    state: str  # Torrent state. See table here below for the possible values
    super_seeding: bool  # True if super seeding is enabled
    tags: str  # Comma-concatenated tag list of the torrent
    time_active: int  # Total active time (seconds)
    total_size: int  # Total size (bytes) of all files in this torrent (including unselected ones)
    # The first tracker with working status. Returns empty string if no tracker is working.
    tracker: str
    up_limit: int  # Torrent upload speed limit (bytes/s). -1 if unlimited.
    uploaded: int  # Amount of data uploaded
    uploaded_session: int  # Amount of data uploaded this session
    upspeed: int  # Torrent upload speed (bytes/s)


class QFUTorrentSettings(BaseModel):
    """QFU torrent info."""

    model_config = ConfigDict(
        extra="forbid",
    )

    tracker_tag: str | None = None
    score: float | int | None = None
    is_hit_and_run: bool | None = None
    is_hard_link: bool | None = None
    is_ok_removal: bool | None = None
    is_pulic: bool | None = None
    is_issue: bool | None = None
    is_cross_seed: bool | None = None


class TorrentInfos(BaseModel):
    api: APITorrentInfos
    qfu: QFUTorrentSettings
