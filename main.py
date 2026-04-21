"""Playlist Sync Suite entrypoint.

This thin wrapper runs the sibling YouTube and Rekordbox projects in sequence,
so the suite does not duplicate their internal code/config.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync YouTube playlists into Rekordbox/m3u8 playlists.")
    parser.add_argument(
        "--only-playlist",
        dest="only_playlist",
        help="Only process the playlist with this exact title.",
    )
    parser.add_argument(
        "--skip-rekordbox",
        dest="skip_rekordbox",
        action="store_true",
        help="Skip Rekordbox XML deduplication and m3u8 export steps.",
    )
    parser.add_argument(
        "--auto-rekordbox",
        dest="auto_rekordbox",
        action="store_true",
        help="Run Rekordbox XML-only automation: backup, delete old playlists, and import new ones.",
    )
    parser.add_argument(
        "--full-auto",
        dest="full_auto",
        action="store_true",
        help=(
            "Run best-effort end-to-end automation, including Rekordbox UI export/import "
            "attempts and XML update monitoring."
        ),
    )
    parser.add_argument(
        "--export-timeout",
        dest="export_timeout",
        type=int,
        default=300,
        help="Seconds to wait for Rekordbox XML export file update in full-auto mode.",
    )
    parser.add_argument(
        "--auto-import-ui",
        dest="auto_import_ui",
        action="store_true",
        help="In full-auto mode, also try to trigger Rekordbox XML import via UI automation.",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Do not download files or write playlists; just log what would happen.",
    )
    parser.add_argument(
        "--use-cache",
        dest="use_cache",
        action="store_true",
        help="Use cached API data when available to avoid quota issues.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    def resolve_project_dir(project_name: str, env_var_name: str) -> Path:
        """
        Resolve where a sibling project lives.

        Priority:
        1) Explicit env var override (absolute or relative path)
        2) default sibling path under repo_root
        """
        env_override = os.environ.get(env_var_name)
        if env_override:
            candidate = Path(env_override).expanduser()
            if not candidate.is_absolute():
                candidate = (Path.cwd() / candidate).resolve()
            return candidate

        return repo_root / project_name

    youtube_dir = resolve_project_dir("youtube", "YOUTUBE_PROJECT_DIR")
    rekordbox_dir = resolve_project_dir("rekordbox", "REKORDBOX_PROJECT_DIR")

    youtube_main = youtube_dir / "main.py"
    rekordbox_main = rekordbox_dir / "main.py"

    if not youtube_main.exists():
        raise FileNotFoundError(
            f"YouTube entrypoint not found at {youtube_main}. "
            "Set YOUTUBE_PROJECT_DIR to the youtube repo path."
        )
    if not rekordbox_main.exists():
        raise FileNotFoundError(
            f"Rekordbox entrypoint not found at {rekordbox_main}. "
            "Set REKORDBOX_PROJECT_DIR to the rekordbox repo path."
        )

    def resolve_project_python(project_dir: Path, env_var_name: str) -> str:
        """
        Resolve which Python interpreter to use for a sibling project.

        Priority:
        1) Explicit env var override (e.g. YOUTUBE_PYTHON)
        2) project-local .venv interpreter
        3) current interpreter (sys.executable)
        """
        env_override = os.environ.get(env_var_name)
        if env_override:
            return env_override

        local_venv_python = project_dir / ".venv" / "bin" / "python"
        if local_venv_python.exists():
            return str(local_venv_python)

        return str(sys.executable)

    youtube_python = resolve_project_python(youtube_dir, "YOUTUBE_PYTHON")
    rekordbox_python = resolve_project_python(rekordbox_dir, "REKORDBOX_PYTHON")

    youtube_cmd = [youtube_python, str(youtube_main)]
    if args.only_playlist:
        youtube_cmd.extend(["--only-playlist", args.only_playlist])
    if args.dry_run:
        youtube_cmd.append("--dry-run")
    if args.use_cache:
        youtube_cmd.append("--use-cache")

    subprocess.run(youtube_cmd, check=True, cwd=youtube_dir)

    if args.skip_rekordbox:
        return

    rekordbox_cmd = [rekordbox_python, str(rekordbox_main)]
    if args.auto_rekordbox:
        rekordbox_cmd.append("--auto-rekordbox")
    if args.full_auto:
        rekordbox_cmd.append("--full-auto")
    if args.auto_import_ui:
        rekordbox_cmd.append("--auto-import-ui")
    if args.export_timeout:
        rekordbox_cmd.extend(["--export-timeout", str(args.export_timeout)])

    subprocess.run(rekordbox_cmd, check=True, cwd=rekordbox_dir)


if __name__ == "__main__":
    main()
