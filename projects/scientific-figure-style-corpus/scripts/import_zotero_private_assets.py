#!/usr/bin/env python3
"""Import the user-authorized Zotero figure asset package into this repository.

This script is intentionally local-first because the ChatGPT GitHub connector does
not expose a binary/LFS upload channel. It verifies the package and every PNG
against the packaged manifest before writing repository files.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import zipfile
from pathlib import Path

EXPECTED_ZIP_SHA256 = "b29f63e9d8feeccb2f80987609d712455289303969241ca7aad55c6415a3eac4"
EXPECTED_PNG_COUNT = 139
PROJECT = Path("projects/scientific-figure-style-corpus")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package", type=Path, help="Path to private-local-assets.zip")
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    package = args.package.expanduser().resolve()
    root = args.repo_root.expanduser().resolve()
    if not package.is_file():
        raise SystemExit(f"Package not found: {package}")
    if sha256_file(package) != EXPECTED_ZIP_SHA256:
        raise SystemExit("Package SHA-256 mismatch; refusing import")

    project = root / PROJECT
    assets_root = project / "assets" / "zotero"
    manifest_out = project / "manifests" / "zotero-private-manifest.csv"
    archive_root = project / "handoff" / "private-local-assets-2026-09-12"

    with zipfile.ZipFile(package) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        png_names = [n for n in names if n.lower().endswith(".png")]
        if len(png_names) != EXPECTED_PNG_COUNT:
            raise SystemExit(f"Expected {EXPECTED_PNG_COUNT} PNGs, found {len(png_names)}")
        if "zotero-private-manifest.csv" not in names:
            raise SystemExit("Package is missing zotero-private-manifest.csv")

        raw_manifest = zf.read("zotero-private-manifest.csv")
        rows = list(csv.DictReader(io.StringIO(raw_manifest.decode("utf-8-sig"))))
        by_sample = {r["sample_id"]: r for r in rows}
        if len(rows) != EXPECTED_PNG_COUNT:
            raise SystemExit(f"Expected {EXPECTED_PNG_COUNT} manifest rows, found {len(rows)}")

        verified = 0
        for name in png_names:
            sample_id = Path(name).stem
            row = by_sample.get(sample_id)
            if row is None:
                raise SystemExit(f"No manifest row for {name}")
            data = zf.read(name)
            got = sha256_bytes(data)
            want = row.get("sha256", "").strip().lower()
            if got != want:
                raise SystemExit(f"SHA-256 mismatch for {name}: {got} != {want}")
            rel = Path(name)
            if rel.parts[0] != "zotero":
                raise SystemExit(f"Unexpected PNG path: {name}")
            dest = assets_root.joinpath(*rel.parts[1:])
            if dest.exists() and not args.overwrite:
                if sha256_file(dest) != got:
                    raise SystemExit(f"Existing asset differs; rerun with --overwrite: {dest}")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            verified += 1

        manifest_out.parent.mkdir(parents=True, exist_ok=True)
        manifest_out.write_bytes(raw_manifest)

        for name in names:
            if name.lower().endswith(".png") or name == "zotero-private-manifest.csv":
                continue
            dest = archive_root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(zf.read(name))

    print(f"Verified and imported {verified} PNG assets")
    print(f"Assets:   {assets_root.relative_to(root)}")
    print(f"Manifest: {manifest_out.relative_to(root)}")
    print(f"QA files: {archive_root.relative_to(root)}")
    print("Next: inspect `git status`, then commit on feat/figure-style-corpus-v0.1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
