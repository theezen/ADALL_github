"""Google Drive helpers for ADALL notebooks (Colab mount + optional shared-folder download)."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Iterable, Optional

# Week 4 expects these CSV names (from Week 3 export folder).
WEEK4_CSV_FILES = (
    "train_features.csv",
    "test_features.csv",
    "train_target.csv",
    "test_target.csv",
)

DEFAULT_XA_FOLDER_NAME = "XA"
DEFAULT_WEEK3_EXPORT_FOLDER = "week3_github_upload"


def mount_google_drive_colab(mount_point: str = "/content/drive") -> str:
    """Mount Google Drive in Google Colab. Returns the mount path."""
    from google.colab import drive

    drive.mount(mount_point)
    return mount_point


def _my_drive_root(mount_point: str = "/content/drive") -> Path:
    return Path(mount_point) / "MyDrive"


def find_folder_by_name(
    folder_name: str,
    *,
    mount_point: str = "/content/drive",
    search_root: Optional[Path] = None,
    max_depth: int = 6,
) -> Optional[Path]:
    """Find the first folder whose name matches (case-insensitive) under My Drive."""
    root = search_root or _my_drive_root(mount_point)
    if not root.exists():
        raise FileNotFoundError(
            f"Drive not mounted or path missing: {root}. Run mount_google_drive_colab() first."
        )

    target = folder_name.casefold()
    root_depth = len(root.parts)

    for dirpath, dirnames, _ in os.walk(root):
        depth = len(Path(dirpath).parts) - root_depth
        if depth > max_depth:
            dirnames.clear()
            continue
        for name in dirnames:
            if name.casefold() == target:
                return Path(dirpath) / name
    return None


def resolve_xa_folder(
    *,
    mount_point: str = "/content/drive",
    folder_name: str = DEFAULT_XA_FOLDER_NAME,
    explicit_path: Optional[str] = None,
) -> Path:
    """
    Resolve the XA (or Week 3 export) folder on mounted Drive.

    Order: explicit_path -> My Drive/<folder_name> -> search My Drive for folder_name.
    """
    if explicit_path:
        path = Path(explicit_path)
        if not path.exists():
            raise FileNotFoundError(f"Drive folder not found: {path}")
        return path

    direct = _my_drive_root(mount_point) / folder_name
    if direct.is_dir():
        return direct

    found = find_folder_by_name(folder_name, mount_point=mount_point)
    if found is not None:
        return found

    raise FileNotFoundError(
        f"Could not find folder '{folder_name}' on Google Drive. "
        f"Tried {direct} and a search under {_my_drive_root(mount_point)}. "
        "Set explicit_path='/content/drive/MyDrive/.../XA' or check the folder name."
    )


def copy_folder(src: Path, dest: Path) -> Path:
    """Copy a Drive folder into the Colab/local workspace."""
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return dest


def download_shared_folder_gdown(folder_id: str, dest: Path) -> Path:
    """
    Download a *public* or *anyone with the link* Google Drive folder by ID.

    Requires: pip install gdown
    """
    import gdown

    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    gdown.download_folder(url, output=str(dest), quiet=False, use_cookies=False)
    return dest


def sync_xa_from_drive(
    local_dir: str = "XA",
    *,
    mount_point: str = "/content/drive",
    folder_name: str = DEFAULT_XA_FOLDER_NAME,
    explicit_path: Optional[str] = None,
) -> Path:
    """Copy the XA folder from mounted Google Drive into the notebook working directory."""
    src = resolve_xa_folder(
        mount_point=mount_point,
        folder_name=folder_name,
        explicit_path=explicit_path,
    )
    return copy_folder(src, Path(local_dir))


def sync_xa_from_shared_link(
    folder_id: str,
    local_dir: str = "XA",
) -> Path:
    """Download shared Drive folder by ID into local_dir (no Colab mount required)."""
    return download_shared_folder_gdown(folder_id, Path(local_dir))


def load_week4_tables_from_folder(folder: Path):
    """Load Week 4 train/test CSVs from a local folder (XA or week3_github_upload)."""
    import pandas as pd

    folder = Path(folder)
    missing = [f for f in WEEK4_CSV_FILES if not (folder / f).is_file()]
    if missing:
        raise FileNotFoundError(
            f"Missing CSV(s) in {folder}: {missing}. "
            f"Expected Week 3 export files: {list(WEEK4_CSV_FILES)}"
        )

    X_train = pd.read_csv(folder / "train_features.csv")
    X_test = pd.read_csv(folder / "test_features.csv")
    y_train_df = pd.read_csv(folder / "train_target.csv")
    y_test_df = pd.read_csv(folder / "test_target.csv")
    return X_train, X_test, y_train_df, y_test_df


def list_csv_files(folder: Path) -> Iterable[str]:
    folder = Path(folder)
    return sorted(p.name for p in folder.glob("*.csv"))
