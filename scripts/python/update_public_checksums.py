#!/usr/bin/env python3
"""Refresh the public SHA256 manifest for Git-tracked archive files."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


DEFAULT_MANIFEST = "logs/hpc_recovery/public_archive_sha256.tsv"

EXCLUDE_PREFIXES = (
    ".git/",
    "sources/",
    "collected_hpc/",
)

EXCLUDE_PATHS = {
    DEFAULT_MANIFEST,
}


def normalize(path: Path | str) -> str:
    return Path(path).as_posix()


def git_ls_files(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_manifest(path: Path) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for line in handle:
            line = line.rstrip("\n\r")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) != 3:
                raise ValueError(f"Invalid manifest row: {line}")
            rows[fields[2]] = (fields[0], fields[1])
    return rows


def should_include(rel: str) -> bool:
    if rel in EXCLUDE_PATHS:
        return False
    return not rel.startswith(EXCLUDE_PREFIXES)


def refresh_rows(repo: Path, manifest: Path, paths: list[str] | None) -> dict[str, tuple[str, str]]:
    rows = read_manifest(manifest)
    targets = paths if paths else git_ls_files(repo)
    for rel in targets:
        rel = normalize(rel)
        if not should_include(rel):
            continue
        path = repo / rel
        if not path.is_file():
            continue
        rows[rel] = (sha256_file(path), str(path.stat().st_size))

    missing = [rel for rel in rows if rel != DEFAULT_MANIFEST and not (repo / rel).exists()]
    for rel in missing:
        del rows[rel]
    return dict(sorted(rows.items(), key=lambda item: item[0].lower()))


def write_manifest(path: Path, rows: dict[str, tuple[str, str]]) -> None:
    content = "".join(f"{digest}\t{size}\t{rel}\n" for rel, (digest, size) in rows.items())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh the public SHA256 manifest.")
    parser.add_argument("--repo", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument(
        "--manifest",
        default=DEFAULT_MANIFEST,
        help=f"Manifest path relative to repo. Defaults to {DEFAULT_MANIFEST}.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional file paths to refresh. Defaults to all Git-tracked files.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    manifest = repo / args.manifest
    try:
        rows = refresh_rows(repo, manifest, args.paths or None)
        write_manifest(manifest, rows)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"Failed to refresh checksum manifest: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {args.manifest} with {len(rows)} tracked file checksums.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
