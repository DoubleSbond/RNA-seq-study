#!/usr/bin/env python3
"""Validate the lightweight public archive state.

This checker is intentionally local-only and GitHub-friendly. It does not
require HPC access and does not inspect raw data outside the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "README.md",
    "CONTRIBUTING.md",
    ".gitattributes",
    ".gitignore",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/archive-gap.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/external-asset.yml",
    ".github/ISSUE_TEMPLATE/hpc-confirmation.yml",
    ".github/ISSUE_TEMPLATE/release-decision.yml",
    ".github/workflows/archive-validation.yml",
    "data/README.md",
    "docs/README.md",
    "docs/workflow.md",
    "docs/archive_status.md",
    "docs/archive_completeness_audit.md",
    "docs/release_blockers.md",
    "docs/release_notes_v0.1_draft.md",
    "docs/release_readiness_checklist.md",
    "docs/hpc_evidence_collection_checklist.md",
    "docs/citation_and_license_decisions.md",
    "docs/citation_cff_draft.md",
    "docs/license_decision_matrix.md",
    "scripts/README.md",
    "scripts/python/README.md",
    "scripts/R/README.md",
    "scripts/shell/README.md",
    "config/README.md",
    "environment/README.md",
    "logs/README.md",
    "logs/hpc_recovery/public_archive_sha256.tsv",
    "results_manifest/README.md",
    "results_manifest/external_assets_manifest.tsv",
]

FORBIDDEN_TRACKED_SUFFIXES = {
    ".fastq",
    ".fq",
    ".bam",
    ".sam",
    ".cram",
    ".fa",
    ".fasta",
    ".fna",
    ".faa",
    ".gff",
    ".gff3",
    ".gtf",
    ".zip",
    ".tar",
    ".tgz",
    ".7z",
    ".rar",
}

FORBIDDEN_TRACKED_ENDINGS = (
    ".fastq.gz",
    ".fq.gz",
    ".tar.gz",
)

ALLOWED_LARGE_TEXT_ASSETS = {
    "logs/unknownCYP/unknownCYP_raw24_peptideAvailable14_17ORFs_Ph36_BmSf.clean_header.LGFR6.log",
    "results_manifest/unknownCYP/unknownCYP_raw24_peptideAvailable14_17ORFs_Ph36_BmSf.clean_header.LGFR6.treefile",
}

PK_START = "BE" + "GIN "
PK_END = " K" + "EY"

SENSITIVE_PATTERNS = [
    re.compile(PK_START + r"[A-Z ]*" + "PRI" + "VATE" + PK_END),
    re.compile("github" + r"_pat_" + r"[A-Za-z0-9_]+"),
    re.compile("ghp" + r"_" + r"[A-Za-z0-9_]+"),
    re.compile("glpat" + r"-" + r"[A-Za-z0-9_-]+"),
    re.compile(r"(?i)\b(password|passwd|secret|token)\s*=\s*[^,\s]+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9_.-]+"),
]


def normalize(path: Path) -> str:
    return path.as_posix()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def git_ls_files(repo: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_required_paths(repo: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (repo / rel).exists():
            fail(errors, f"missing required path: {rel}")
    return errors


def check_checksums(repo: Path) -> list[str]:
    errors: list[str] = []
    manifest = repo / "logs/hpc_recovery/public_archive_sha256.tsv"
    if not manifest.exists():
        return ["missing checksum manifest: logs/hpc_recovery/public_archive_sha256.tsv"]

    seen: set[str] = set()
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        for lineno, line in enumerate(handle, start=1):
            line = line.rstrip("\n\r")
            if not line:
                continue
            fields = line.split("\t")
            if len(fields) != 3:
                fail(errors, f"checksum manifest line {lineno} does not have 3 columns")
                continue
            expected_hash, expected_size, rel = fields
            seen.add(rel)
            path = repo / rel
            if not path.exists():
                fail(errors, f"checksum target missing: {rel}")
                continue
            try:
                size = path.stat().st_size
                parsed_size = int(expected_size)
            except ValueError:
                fail(errors, f"checksum manifest line {lineno} has invalid size: {expected_size}")
                continue
            if size != parsed_size:
                fail(errors, f"size mismatch for {rel}: manifest {parsed_size}, actual {size}")
            actual_hash = sha256_file(path)
            if actual_hash != expected_hash:
                fail(errors, f"sha256 mismatch for {rel}")

    for rel in REQUIRED_PATHS:
        if rel in {".gitignore", "logs/hpc_recovery/public_archive_sha256.tsv"}:
            continue
        if rel.endswith(".md") and rel not in seen:
            fail(errors, f"required documentation file not listed in checksum manifest: {rel}")
    return errors


def check_tracked_file_policy(repo: Path) -> list[str]:
    errors: list[str] = []
    tracked = git_ls_files(repo)
    for rel in tracked:
        lower = rel.lower()
        if rel in ALLOWED_LARGE_TEXT_ASSETS:
            continue
        if lower.endswith(FORBIDDEN_TRACKED_ENDINGS) or Path(lower).suffix in FORBIDDEN_TRACKED_SUFFIXES:
            fail(errors, f"forbidden large/raw-data file is tracked by Git: {rel}")
    return errors


def should_scan(rel: str, path: Path, max_bytes: int) -> bool:
    if rel.startswith(("sources/", ".git/")):
        return False
    if path.is_dir() or path.stat().st_size > max_bytes:
        return False
    return True


def check_sensitive_patterns(repo: Path, max_bytes: int) -> list[str]:
    errors: list[str] = []
    tracked = git_ls_files(repo)
    candidates = tracked or [
        normalize(path.relative_to(repo))
        for path in repo.rglob("*")
        if ".git" not in path.parts and "sources" not in path.parts
    ]
    for rel in candidates:
        path = repo / rel
        if not path.exists() or not should_scan(rel, path, max_bytes):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                fail(errors, f"possible sensitive pattern in {rel}: {pattern.pattern}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the public CYP archive state.")
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository root to validate. Defaults to the current directory.",
    )
    parser.add_argument(
        "--max-sensitive-scan-bytes",
        type=int,
        default=1_000_000,
        help="Maximum file size to scan for sensitive text patterns.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    checks = [
        ("required paths", check_required_paths(repo)),
        ("checksum manifest", check_checksums(repo)),
        ("tracked file policy", check_tracked_file_policy(repo)),
        ("sensitive text scan", check_sensitive_patterns(repo, args.max_sensitive_scan_bytes)),
    ]

    errors: list[str] = []
    for name, check_errors in checks:
        if check_errors:
            print(f"[FAIL] {name}")
            for error in check_errors:
                print(f"  - {error}")
            errors.extend(check_errors)
        else:
            print(f"[ OK ] {name}")

    if errors:
        print(f"\nArchive validation failed with {len(errors)} issue(s).")
        return 1
    print("\nArchive validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
