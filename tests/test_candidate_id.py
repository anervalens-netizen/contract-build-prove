import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "candidate_id.py"


def run(cmd, cwd, check=True, env=None):
    result = subprocess.run(
        cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {cmd}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return result


class CandidateIdTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        run(["git", "init", "-q"], self.root)
        run(["git", "config", "user.email", "cbp@example.test"], self.root)
        run(["git", "config", "user.name", "CBP Test"], self.root)
        (self.root / "tracked.txt").write_text("base\n")
        (self.root / "binary.bin").write_bytes(b"\x00base\xff")
        run(["git", "add", "."], self.root)
        run(["git", "commit", "-qm", "base"], self.root)
        self.base_branch = run(["git", "branch", "--show-current"], self.root).stdout.strip()

    def tearDown(self):
        self.tmp.cleanup()

    def create(self, *extra, check=True):
        return run([sys.executable, str(SCRIPT), "create", *extra], self.root, check=check)

    def candidate(self, *extra):
        return json.loads(self.create(*extra).stdout)["candidate_id"]

    def test_tracked_staged_unstaged_binary_rename_delete_change_identity(self):
        base = self.candidate()
        (self.root / "tracked.txt").write_text("unstaged\n")
        self.assertNotEqual(base, self.candidate())
        run(["git", "add", "tracked.txt"], self.root)
        staged = self.candidate()
        self.assertNotEqual(base, staged)
        (self.root / "binary.bin").write_bytes(b"\x00changed\xfe")
        self.assertNotEqual(staged, self.candidate())
        run(["git", "mv", "tracked.txt", "renamed.txt"], self.root)
        renamed = self.candidate()
        self.assertNotEqual(staged, renamed)
        (self.root / "binary.bin").unlink()
        self.assertNotEqual(renamed, self.candidate())

    def test_untracked_content_mode_and_symlink_change_identity(self):
        (self.root / "new.sh").write_text("#!/bin/sh\necho hi\n")
        first = self.candidate()
        os.chmod(self.root / "new.sh", 0o755)
        second = self.candidate()
        self.assertNotEqual(first, second)
        if hasattr(os, "symlink"):
            os.symlink("tracked.txt", self.root / "link")
            third = self.candidate()
            os.unlink(self.root / "link")
            os.symlink("binary.bin", self.root / "link")
            fourth = self.candidate()
            self.assertNotEqual(third, fourth)

    def test_literal_exclude_only_excludes_requested_path(self):
        special = self.root / "control[1].md"
        special.write_text("one\n")
        excluded = self.candidate("--exclude", "control[1].md")
        special.write_text("two\n")
        self.assertEqual(excluded, self.candidate("--exclude", "control[1].md"))
        other = self.root / "control1.md"
        other.write_text("x\n")
        self.assertNotEqual(excluded, self.candidate("--exclude", "control[1].md"))

    def test_verify_match_and_mismatch(self):
        expected = self.candidate()
        self.assertEqual(0, run([sys.executable, str(SCRIPT), "verify", expected], self.root).returncode)
        (self.root / "tracked.txt").write_text("changed\n")
        self.assertEqual(
            2,
            run([sys.executable, str(SCRIPT), "verify", expected], self.root, check=False).returncode,
        )

    def assert_unsupported(self, reason_fragment):
        result = self.create(check=False)
        self.assertEqual(3, result.returncode, msg=result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("UNSUPPORTED_WORKTREE_STATE", payload["error"])
        self.assertIn(reason_fragment, payload["reason"])

    def test_unresolved_conflict_rejected(self):
        run(["git", "checkout", "-qb", "other"], self.root)
        (self.root / "tracked.txt").write_text("other\n")
        run(["git", "commit", "-qam", "other"], self.root)
        run(["git", "checkout", "-q", self.base_branch], self.root)
        (self.root / "tracked.txt").write_text("base-branch\n")
        run(["git", "commit", "-qam", "base-branch"], self.root)
        self.assertNotEqual(0, run(["git", "merge", "other"], self.root, check=False).returncode)
        self.assert_unsupported("UNRESOLVED_CONFLICTS")

    def test_assume_unchanged_rejected(self):
        run(["git", "update-index", "--assume-unchanged", "tracked.txt"], self.root)
        self.assert_unsupported("ASSUME_UNCHANGED")

    def test_skip_worktree_rejected(self):
        run(["git", "update-index", "--skip-worktree", "tracked.txt"], self.root)
        self.assert_unsupported("SKIP_WORKTREE")

    def test_core_filemode_false_rejected(self):
        run(["git", "config", "core.fileMode", "false"], self.root)
        self.assert_unsupported("CORE_FILEMODE_FALSE")

    def test_dirty_submodule_rejected(self):
        with tempfile.TemporaryDirectory() as sub_tmp:
            sub = Path(sub_tmp)
            run(["git", "init", "-q"], sub)
            run(["git", "config", "user.email", "sub@example.test"], sub)
            run(["git", "config", "user.name", "Sub Test"], sub)
            (sub / "x.txt").write_text("base\n")
            run(["git", "add", "."], sub)
            run(["git", "commit", "-qm", "base"], sub)
            run(
                ["git", "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(sub), "vendor/sub"],
                self.root,
            )
            run(["git", "commit", "-qam", "add submodule"], self.root)
            (self.root / "vendor/sub/x.txt").write_text("dirty\n")
            self.assert_unsupported("DIRTY_SUBMODULE")


if __name__ == "__main__":
    unittest.main()
