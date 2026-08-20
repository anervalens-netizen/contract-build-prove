#!/usr/bin/env python3
"""Create or verify a deterministic identity for an uncommitted CBP candidate.

Uses Git plus Python stdlib only. Prefer an exact commit SHA when local commits are
permitted; use this helper only when the candidate must remain uncommitted.
"""

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

VERSION = "cbp1"


def git(args, cwd=None):
    result = subprocess.run(
        ["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode:
        sys.stderr.buffer.write(result.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def repo_root():
    return Path(git(["rev-parse", "--show-toplevel"]).decode().strip()).resolve()


def normalize_excludes(root, values):
    excludes = []
    for raw in values:
        path = Path(raw)
        if path.is_absolute():
            try:
                path = path.resolve().relative_to(root)
            except Exception:
                raise SystemExit(f"exclude outside repository: {raw}")
        normalized = path.as_posix().strip("/")
        if normalized and normalized not in excludes:
            excludes.append(normalized)
    return sorted(excludes, key=os.fsencode)


def is_excluded(path, excludes):
    return any(path == item or path.startswith(item + "/") for item in excludes)


def git_mode_and_content(path):
    info = os.lstat(path)
    if stat.S_ISLNK(info.st_mode):
        target = os.readlink(path).encode("utf-8", "surrogateescape")
        return b"120000", target
    if stat.S_ISREG(info.st_mode):
        mode = b"100755" if info.st_mode & 0o111 else b"100644"
        return mode, path.read_bytes()
    raise SystemExit(f"unsupported untracked file type: {path}")


def compute(root, excludes):
    head = git(["rev-parse", "HEAD"], root).decode().strip()

    diff_args = [
        "diff",
        "--binary",
        "--no-ext-diff",
        "--no-textconv",
        "HEAD",
        "--",
        ".",
    ]
    for item in excludes:
        diff_args += [f":(exclude){item}", f":(exclude){item}/**"]
    tracked_patch_hash = hashlib.sha256(git(diff_args, root)).hexdigest()

    raw_paths = git(["ls-files", "--others", "--exclude-standard", "-z"], root)
    paths = sorted(path for path in raw_paths.split(b"\0") if path)
    manifest = bytearray()

    for path_bytes in paths:
        relative = os.fsdecode(path_bytes)
        if is_excluded(Path(relative).as_posix(), excludes):
            continue
        mode, content = git_mode_and_content(root / relative)
        content_hash = hashlib.sha256(content).hexdigest().encode()
        manifest += path_bytes + b"\0" + mode + b"\0" + content_hash + b"\0"

    untracked_manifest_hash = hashlib.sha256(manifest).hexdigest()
    control_blob = b"\0".join(os.fsencode(item) for item in excludes)
    record = b"\0".join(
        [
            VERSION.encode(),
            head.encode(),
            tracked_patch_hash.encode(),
            untracked_manifest_hash.encode(),
            control_blob,
        ]
    )
    candidate_id = f"{VERSION}:{hashlib.sha256(record).hexdigest()}"

    return {
        "candidate_id": candidate_id,
        "base_head": head,
        "tracked_patch_sha256": tracked_patch_hash,
        "untracked_manifest_sha256": untracked_manifest_hash,
        "control_state_paths": excludes,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Create or verify a deterministic CBP candidate identity."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument(
        "--exclude", action="append", default=[], help="Control-state path; repeatable."
    )

    verify = sub.add_parser("verify")
    verify.add_argument("expected", help="Expected cbp1:<sha256> identity.")
    verify.add_argument(
        "--exclude", action="append", default=[], help="Control-state path; repeatable."
    )

    args = parser.parse_args()
    root = repo_root()
    excludes = normalize_excludes(root, args.exclude)
    result = compute(root, excludes)

    if args.command == "create":
        print(json.dumps(result, separators=(",", ":"), sort_keys=True))
        return 0

    matches = result["candidate_id"] == args.expected
    print(
        json.dumps(
            {
                "match": matches,
                "expected": args.expected,
                "actual": result["candidate_id"],
                "details": result,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0 if matches else 2


if __name__ == "__main__":
    raise SystemExit(main())
