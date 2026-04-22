# Playlist Sync Suite

Runs two independent projects in sequence:
1. Download/sync playlists locally from YouTube
2. Sync those playlists into Rekordbox XML

This suite orchestrates:
- https://github.com/alexandrosnic/youtube-playlist-downloader
- https://github.com/alexandrosnic/rekordbox-playlist-sync
- https://github.com/alexandrosnic/playlist-sync-suite

## Setup
This repo has no local config. Configure the sibling projects instead:
- YouTube: `youtube/config/playlist_path.json` -> `youtube_paths.youtube_playlist_m3u8_dir`
- Rekordbox: `rekordbox/config/playlist_path.json` -> `sync_paths.source_playlist_m3u8_dir`
- Rekordbox: `rekordbox/config/playlist_path.json` -> `sync_paths.rekordbox_custom_playlists_m3u8_dir`
- Rekordbox: `rekordbox/config/playlist_path.json` -> `sync_paths.xml_library_path`

Install each sibling project's dependencies once:

```bash
cd ../youtube
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
deactivate

cd ../rekordbox
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
deactivate
```

## Run
```bash
python3 main.py
```

The suite uses each sibling project's `.venv` Python if available, otherwise it falls back to the current interpreter.

Optional overrides:
- `YOUTUBE_PROJECT_DIR=/abs/path/to/youtube`: use this when the YouTube repo is not in the default sibling path (`../youtube`).
- `REKORDBOX_PROJECT_DIR=/abs/path/to/rekordbox`: use this when the Rekordbox repo is not in the default sibling path (`../rekordbox`).
- `YOUTUBE_PYTHON=/abs/path/to/python`: force a specific Python interpreter for the YouTube step (for example a custom venv/conda env).
- `REKORDBOX_PYTHON=/abs/path/to/python`: force a specific Python interpreter for the Rekordbox step.

If you do not set these, the suite auto-detects sibling folders and uses each project's local `.venv` Python when available.

## CLI options
- `--only-playlist "Playlist Name"`: pass through to YouTube project; process one playlist by exact title
- `--dry-run`: pass through to YouTube project; no downloads or playlist writes
- `--use-cache`: pass through to YouTube project; prefer cached API data when available
- `--skip-rekordbox`: run only YouTube project and skip Rekordbox step
- `--auto-rekordbox`: pass through to Rekordbox project XML-only automated flow
- `--full-auto`: pass through to Rekordbox best-effort UI + XML automation flow
- `--export-timeout 300`: pass through timeout (seconds) used by Rekordbox full-auto export watcher
- `--auto-import-ui`: with `--full-auto`, attempt Rekordbox UI-triggered XML import

## Notes
- This repo calls `youtube/main.py` and `rekordbox/main.py` directly
- It can be published independently, but it depends on those two sibling repos at runtime
