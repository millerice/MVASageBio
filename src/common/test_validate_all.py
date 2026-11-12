"""Synthetic regressions for the git-history leak scan (temporary repositories only)."""
import subprocess
import tempfile
import unittest
from pathlib import Path

import validate_all

# Assembled at runtime so this file never contains a literal match for the scanner.
SYNTHETIC_HGVS = "c." + "123" + "A>G"
SYNTHETIC_ROW = "PROBAND01,chr7," + "7000001" + ",T,G"


def git(repo, *args):
    subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                    "-c", "commit.gpgsign=false", *args], cwd=repo, check=True,
                   capture_output=True)


class HistoryLeakTests(unittest.TestCase):
    def make_repo(self, directory):
        repo = Path(directory)
        git(repo, "init", "-q")
        return repo

    def test_clean_history_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(directory)
            (repo / "report.md").write_text("Gene-level conclusion only.\n")
            git(repo, "add", ".")
            git(repo, "commit", "-q", "-m", "clean")
            self.assertEqual(validate_all.history_leaks(repo), [])

    def test_content_removed_from_working_tree_is_still_found(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(directory)
            (repo / "report.md").write_text(f"Allele 1: {SYNTHETIC_HGVS}\n")
            git(repo, "add", ".")
            git(repo, "commit", "-q", "-m", "draft")
            (repo / "report.md").write_text("Allele 1: <redacted>\n")
            git(repo, "commit", "-q", "-am", "scrub working tree")
            self.assertIn(("report.md", "coding HGVS"), validate_all.history_leaks(repo))

    def test_commit_message_and_data_row_are_found(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(directory)
            (repo / "notes.md").write_text(SYNTHETIC_ROW + "\n")
            git(repo, "add", ".")
            git(repo, "commit", "-q", "-m", f"lock {SYNTHETIC_HGVS}")
            labels = {label for _, label in validate_all.history_leaks(repo)}
            self.assertLessEqual({"coding HGVS", "T1 data row"}, labels)

    def test_official_template_example_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.make_repo(directory)
            (repo / "template.csv").write_text("PROBAND01,chr1,100000,A,T,chr1,200000,G,C,0.90,primary,\n"
                                               "bcftools view -r chr15:40000000-40100000\n")
            git(repo, "add", ".")
            git(repo, "commit", "-q", "-m", "template")
            self.assertEqual(validate_all.history_leaks(repo), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
