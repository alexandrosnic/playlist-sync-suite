# Playlist Sync Suite

Runs both projects in sequence:
1. YouTube downloader sync
2. Rekordbox XML sync

## Entrypoint
- main.py

## Run
```pwsh
python3 main.py
```

## One-time setup
```pwsh
# YouTube project env
cd ../youtube
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
deactivate

# Rekordbox project env
cd ../rekordbox
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
deactivate
```

## Daily run (no activation required)
```pwsh
cd ../playlist_sync_suite
python3 main.py
```

You can deactivate after setup because this suite calls each sibling project
with its own interpreter path directly.

This project uses the sibling projects directly:
- youtube/main.py
- rekordbox/main.py

All config is owned by those two projects. There is no local `config/` here.

Interpreter selection used by the suite:
- Uses `../youtube/.venv/bin/python` for YouTube if present.
- Uses `../rekordbox/.venv/bin/python` for Rekordbox if present.
- Falls back to the current Python interpreter if project venv is missing.
- Optional overrides via env vars:
  - `YOUTUBE_PYTHON=/abs/path/to/python`
  - `REKORDBOX_PYTHON=/abs/path/to/python`

Project location overrides (useful when repos are not sibling folders):
- `YOUTUBE_PROJECT_DIR=/abs/path/to/youtube-repo`
- `REKORDBOX_PROJECT_DIR=/abs/path/to/rekordbox-repo`

## Split repositories and cloning
Repository URLs:
- YouTube: `git@github.com:alexandrosnic/youtube-playlist-downloader.git`
- Rekordbox: `git@github.com:alexandrosnic/rekordbox-playlist-sync.git`
- Suite: `git@github.com:alexandrosnic/playlist-sync-suite.git`

```pwsh
mkdir playlist-sync-workspace
cd playlist-sync-workspace

# clone all three repos as siblings
git clone git@github.com:alexandrosnic/youtube-playlist-downloader.git youtube
git clone git@github.com:alexandrosnic/rekordbox-playlist-sync.git rekordbox
git clone git@github.com:alexandrosnic/playlist-sync-suite.git playlist_sync_suite
```

If your folder layout is different, export project paths before running the suite:

```pwsh
export YOUTUBE_PROJECT_DIR=/abs/path/to/youtube
export REKORDBOX_PROJECT_DIR=/abs/path/to/rekordbox
cd /abs/path/to/playlist_sync_suite
python3 main.py
```

## Useful options
- --only-playlist "Playlist Name"
- --skip-rekordbox
- --auto-rekordbox
- --full-auto
- --auto-import-ui

## Project structure
- main.py
- README.md
- requirements.txt

This folder is self-contained and can be published as its own repository.
