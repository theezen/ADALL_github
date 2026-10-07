#!/usr/bin/env python3
"""Download the XA XAUUSD EA project from a shared Google Drive folder."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEST = ROOT / "xa_ea_project"


def main() -> int:
    folder_id = os.environ.get("GOOGLE_DRIVE_XA_EA_FOLDER_ID", "").strip()
    if not folder_id:
        print(
            "Set GOOGLE_DRIVE_XA_EA_FOLDER_ID to the Drive folder ID "
            "(from https://drive.google.com/drive/folders/<ID>).",
            file=sys.stderr,
        )
        return 1

    dest = Path(os.environ.get("XA_EA_DEST", str(DEFAULT_DEST)))
    try:
        import gdown
    except ImportError:
        print("Install gdown: pip install gdown", file=sys.stderr)
        return 1

    dest.mkdir(parents=True, exist_ok=True)
    url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    print(f"Downloading to {dest} ...")
    gdown.download_folder(url, output=str(dest), quiet=False, use_cookies=False)
    print("Done. Verify team/ACCESS_TEST.md and .mq5 files exist under:", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
