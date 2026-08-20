#!/usr/bin/env python3
"""Create or verify a deterministic identity for an uncommitted CBP candidate.

Prefer an exact commit SHA. This helper is only for candidates that must remain
uncommitted. It fails closed on Git states it cannot identify exactly.
"""

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

VERSION = "cbp2"
EXIT_MISMATCH = 2
EXIT_UNSUPPORTED = 3


class UnsupportedState(RuntimeError):
    pass


def run_git(args, cwd=None, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode:
        sys.stderr.buffer.write(result.stderr)
        raise SystemExit(result.returncode)
    return result


def git(args, cwd=None):
    return run_git(args, cwd=cwd).stdout


def repo_root():
    return Path(git(["rev-parse", "--show-toplevel"]).decode().strip()).resolve()


def normalize_excludes(root, values):
    excludes = []
    for raw in values:
        path = Path(raw)
        if path.is_absolute():
            try:
                path = path.resolve().relative_to(root)
            except Exception as exc:
                raise SystemExit(f"exclude outside repository: {raw}") from exc
        normalized = path.as_posix().strip("/")
        if normalized and normalized not in excludes:
            excludes.append(normalized)
    return sorted(excludes, key=os.fsencode)


def is_excluded(path, excludes):
    return any(path == item or path.startswith(item + "/") for item in excludes)


def reject_unsupported_index_state(root):
    if git(["ls-files", "-u", "-z"], root):
        raise UnsupportedState("UNRESOLVED_CONFLICTS")

    raw = git(["ls-files", "-v", "-z"], root)
    for record in (item for item in raw.split(b"\0") if item):
        if len(record) < 3 or record[1:2] != b" ":
            continue
        marker = chr(record[0])
        path = os.fsdecode(record[2:])
        if marker.islower():
            raise UnsupportedState(f"ASSUME_UNCHANGED:{path}")
        if marker.upper() == "S":
            raise UnsupportedState(f"SKIP_WORKTREE:{path}")

    filemode = run_git(["config", "--bool", "--get", "core.fileMode"], root, check=False)
    if filemode.returncode == 0 and filemode.stdout.strip().lower() == b"false":
        raise UnsupportedState("CORE_FILEMODE_FALSE")


def submodule_paths(root):
    raw = git(["ls-files", "-s", "-z"], root)
    paths = []
    for record in (item for item in raw.split(b"\0") if item):
        try:
            meta, path_bytes = record.split(b"\t", 1)
            mode = meta.split(b" ", 1)[0]
        except ValueError:
            continue
        if mode == b"160000":
            paths.append(os.fsdecode(path_bytes))
    return paths


def reject_dirty_submodules(root):
    for relative in submodule_paths(root):
        path = root / relative
        if not path.exists():
            raise UnsupportedState(f"UNINITIALIZED_SUBMODULE:{relative}")
        inside = run_git(["rev-parse", "--is-inside-work-tree"], path, check=False)
        if inside.returncode != 0 or inside.stdout.strip() != b"true":
            raise UnsupportedState(f"UNAVAILABLE_SUBMODULE:{relative}")
        status = git(
            ["status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none"],
            path,
        )
        if status:
            raise UnsupportedState(f"DIRTY_SUBMODULE:{relative}")


def reject_unsupported_state(root):
    reject_unsupported_index_state(root)
    reject_dirty_submodules(root)


def git_mode_and_content(path):
    info = os.lstat(path)
    if stat.S_ISLNK(info.st_mode):
        target = os.readlink(path).encode("utf-8", "surrogateescape")
        return b"120000", target
    if stat.S_ISREG(info.st_mode):
        mode = b"100755" if info.st_mode & 0o111 else b"100644"
        return mode, path.read_bytes()
    raise UnsupportedState(f"UNSUPPORTED_UNTRACKED_TYPE:{path}")


def compute(root, excludes):
    reject_unsupported_state(root)

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
        diff_args.append(f":(top,exclude,literal){item}")
    tracked_patch_hash = hashlib.sha256(git(diff_args, root)).hexdigest()

    raw_paths = git(["ls-files", "--others", "--exclude-standard", "-z"], root)
    paths = sorted((path for path in raw_paths.split(b"\0") if path), key=lambda x: x)
    manifest = bytearray()

    for path_bytes in paths:
        relative = os.fsdecode(path_bytes)
        relative_posix = Path(relative).as_posix()
        if is_excluded(relative_posix, excludes):
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


def emit_unsupported(exc):
    print(
        json.dumps(
            {"error": "UNSUPPORTED_WORKTREE_STATE", "reason": str(exc)},
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return EXIT_UNSUPPORTED


def main():
    parser = argparse.ArgumentParser(
        description="Create or verify an exact CBP identity for an uncommitted candidate."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument(
        "--exclude", action="append", default=[], help="Literal control-state path; repeatable."
    )

    verify = sub.add_parser("verify")
    verify.add_argument("expected", help="Expected cbp2:<sha256> identity.")
    verify.add_argument(
        "--exclude", action="append", default=[], help="Literal control-state path; repeatable."
    )

    args = parser.parse_args()
    root = repo_root()
    excludes = normalize_excludes(root, args.exclude)

    try:
        result = compute(root, excludes)
    except UnsupportedState as exc:
        return emit_unsupported(exc)

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
    return 0 if matches else EXIT_MISMATCH


if __name__ == "__main__":
    raise SystemExit(main())
