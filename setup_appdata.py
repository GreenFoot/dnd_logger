"""One-time script to copy existing data to %APPDATA%\\DnDLogger.

Usage:
    python setup_appdata.py            # skip files that already exist
    python setup_appdata.py --force    # overwrite with source if source is newer
"""

import os
import shutil
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "DnDLogger")

FILES = ("config.json",)
DIRS = ["campaigns"]


def main():
    force = "--force" in sys.argv

    os.makedirs(DEST, exist_ok=True)
    print(f"Source:      {SRC}")
    print(f"Destination: {DEST}")
    print(f"Mode:        {'force (overwrite if newer)' if force else 'safe (skip existing)'}\n")

    for name in FILES:
        src = os.path.join(SRC, name)
        dst = os.path.join(DEST, name)
        if not os.path.exists(src):
            print(f"  SKIP  {name} (not found in source)")
        elif not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"  COPY  {name}")
        elif force:
            shutil.copy2(src, dst)
            print(f"  OVERWRITE  {name}")
        else:
            print(f"  SKIP  {name} (already exists, use --force to overwrite)")

    for name in DIRS:
        src_dir = os.path.join(SRC, name)
        dst_dir = os.path.join(DEST, name)
        if not os.path.isdir(src_dir):
            print(f"  SKIP  {name}/ (not found in source)")
        elif not os.path.exists(dst_dir):
            shutil.copytree(src_dir, dst_dir)
            size_mb = sum(os.path.getsize(os.path.join(r, f)) for r, _, files in os.walk(dst_dir) for f in files) / (
                1024 * 1024
            )
            print(f"  COPY  {name}/ ({size_mb:.1f} MB)")
        elif force:
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
            print(f"  MERGE  {name}/ (added missing files)")
        else:
            print(f"  SKIP  {name}/ (already exists, use --force to overwrite)")

    print(f"\nDone. The exe will read data from:\n  {DEST}")


if __name__ == "__main__":
    main()
