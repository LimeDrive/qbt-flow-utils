# Tracker Configuration Options

This document provides an explanation of the options available in the sample tracker configuration file. Use this as a reference when customizing your own tracker configurations.

## `extra_score`

- **Type:** Integer
- **Required:** Yes
- **Default:** 0

The additional score assigned to this tracker. Higher scores prioritize this tracker when choosing which torrents to remove.

## `tracker_keywords`

- **Type:** List of Strings
- **Required:** Yes

A list of string keywords that will be used to identify torrents from this tracker.

## `hit_and_run`

- **Type:** Object
- **Required:** Yes (at least one option is required)

Options related to hit-and-run torrent management.

### `ignore_hit_and_run`

- **Type:** Boolean
- **Required:** Yes
- **Default:** True

Specifies whether to ignore hit-and-run torrents for this tracker.

### `min_seed_time`

- **Type:** Integer
- **Required:** No

The minimum amount of time in hours that a torrent should be seeded before considering it for removal.

### `min_ratio`

- **Type:** Float
- **Required:** No

The minimum seeding ratio that a torrent should achieve before considering it for removal.

## `auto_manage`

- **Type:** Object
- **Required:** No

Options related to automatic management of torrents based on various conditions.

### `conditions`

- **Type:** Object
- **Required:** No

Conditions that need to be met for the auto management actions to be applied.

#### `max_seed_time`

- **Type:** Integer
- **Required:** No

Maximum seed time in hours for a torrent to be considered eligible for auto management actions.

#### `max_ratio`

- **Type:** Float
- **Required:** No

Maximum seeding ratio for a torrent to be considered eligible for auto management actions.

#### `min_active_seeder`

- **Type:** Integer
- **Required:** No

Minimum number of active seeders for a torrent to be considered eligible for auto management actions.

#### `protect_hit_and_run`

- **Type:** Boolean
- **Required:** No
- **Default:** False

Specifies whether to protect hit-and-run torrents from auto management actions.

### `action`

- **Type:** Object
- **Required:** No

The auto management action to be applied if conditions are met.

#### `limit_upload_speed`

- **Type:** Integer
- **Required:** No

Limit the upload speed in KB/s for torrents matching the conditions.

#### `pause_torrent`, `stop_torrent`, `move_to_local`, `sync_to_remote`, `remove_torrent`

- **Type:** Boolean
- **Required:** No

Various actions that can be taken based on the conditions. Only one of these should be set to `True`.

Please consult the [official documentation](https://LimeDrive.github.io/qbt-flow-utils/) for more details and advanced usage of these configuration options.
