
# **Work in Progress:** qbt-flow-utils

[![Release](https://img.shields.io/github/v/release/LimeDrive/qbt-flow-utils)](https://img.shields.io/github/v/release/LimeDrive/qbt-flow-utils)
[![Build status](https://img.shields.io/github/actions/workflow/status/LimeDrive/qbt-flow-utils/main.yml?branch=main)](https://github.com/LimeDrive/qbt-flow-utils/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/LimeDrive/qbt-flow-utils)](https://img.shields.io/github/commit-activity/m/LimeDrive/qbt-flow-utils)
[![License](https://img.shields.io/github/license/LimeDrive/qbt-flow-utils)](https://img.shields.io/github/license/LimeDrive/qbt-flow-utils)

This project offers automated torrent flow management through auto-tagging, disk space optimization, torrent and cross-seed management, media folder hygiene, tracker automation, and more to come.

- **Github repository**: <https://github.com/LimeDrive/qbt-flow-utils/>
- **Documentation** <https://LimeDrive.github.io/qbt-flow-utils/>

## qBittorrent Automation and Disk Management

This project is designed to interact with qBittorrent in order to automate various tasks and efficiently manage disk space. The primary features of the project include:

### 1. Auto-tagging of Torrents

- Automatically verifies and applies new tags during each run, optimizing API calls.
- Adds appropriate tags based on trackers associated with torrents.
- Adds a "no-hardlink" tag for torrents without physical links.
- Work in progress: Implements tags for tracker-related issues (requires careful API management).
- Adds the "H&R" (Hit and Run) tag for torrents.
- Tags torrents with public trackers accordingly.

### 2. Disk Space Checking

- Monitors and manages available disk space.

### 3. Intelligent Torrent Removal

The script is responsible for freeing up disk space by removing torrents and their cross-seeds, following these steps:

- Maintains a total disk space occupancy within a configurable maximum percentage.
- Considers tracker preferences set by users, seeders, ratio, seed time, and Hit and Run configurations.
- Optionally verifies successful upload through rclone before deleting.
- Checks for associated cross-seeds.
- Deletes torrents and files if deletion criteria are met.
- Removes associated cross-seeds.
- Eliminates physical links to ensure effective deletion, optimizing disk space and bandwidth usage.

### 4. Local Media Folder Inspection

- Inspects the local media folder to ensure it only contains physical links.
- Deletes files not meeting the criteria specified in the configuration.
- Facilitates adding external files to *arr systems, which will later be seamlessly uploaded to the cloud.

### 5. Automatic Tracker Management

- Manages sharing limits and pausing based on specific settings for each tracker.
- Configurations are tailored to peer tracker management.

### 6. Recycle Bin for qBit Metadata

- Setting up a recycle bin (.recyclebin) for deleted metadata from qBittorrent.

### 7. Orphaned File Cleanup

- Checks and removes orphaned files from the seed folder.

### 666. Mutch more to come, feel free to sugeste

This project streamlines torrent management, enhances disk space efficiency, and automates several key processes in conjunction with qBittorrent, *arr systems, and cloudplow. By employing intelligent tagging, disk space monitoring, and seamless removal of torrents, the system ensures optimal performance and resource utilization.

Feel free to contribute, offer suggestions, or use this project to enhance your torrent management experience!

![Static Badge](https://img.shields.io/badge/LimeCat-on_the_Hub's-red?style=for-the-badge&logo=caterpillar&logoColor=%23ffffff)
