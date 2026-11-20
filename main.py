#!/usr/bin/env python3
"""make.fun news-image-20261119 entry.

Renders the deliverable by copying the front-page PNG that ships in this
repository (entry.png, drawn by build_image.py from the verified news of
Thursday 19 November 2026) to the harness output path, then proving the
copy is exact. Standard library only; no network, no randomness.
"""
import hashlib
import os
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEST_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    raw = source.read_bytes()
    if not raw.startswith(PNG_MAGIC):
        print(f"{source}: not a PNG file", file=sys.stderr)
        return 1
    if len(raw) > 1_048_576:
        print(f"{source}: over the 1 MiB cap", file=sys.stderr)
        return 1
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    dest = out / DEST_NAME
    dest.write_bytes(raw)
    if digest(source) != digest(dest):
        print("copy mismatch: refusing to report success", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(raw)} bytes, sha256 {digest(dest)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
