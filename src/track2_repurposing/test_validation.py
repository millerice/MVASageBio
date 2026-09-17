"""Synthetic regressions for citation rejection and non-mutating ranking checks."""
import contextlib
import csv
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import score_candidates as ranking
import validate_chain as chain


def write_tsv(path, rows, fields=None):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


class ClaimValidationTests(unittest.TestCase):
    def run_case(self, refs, empty=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reports = root / "reports"
            reports.mkdir()
            claim_text = "Synthetic claim for citation validation"
            (reports / "report.md").write_text(claim_text + " [EV-0001]\n")
            (root / "chain.json").write_text(json.dumps({
                "nodes": [{"id": "N1", "claim_type": "fact", "granularity": "public",
                           "ev_refs": ["EV-0001"]}], "edges": []}))
            (root / "ledger.jsonl").write_text(json.dumps({
                "id": "EV-0001", "tier": 0, "claim_type": "fact",
                "verification_status": "verified"}) + "\n")
            claim = dict(claim_id="CL-TEST", report_file="reports/report.md",
                         claim_text=claim_text, claim_type="fact", ev_refs=refs,
                         quantitative="no", review_status="machine_checked")
            write_tsv(root / "claims.tsv", [] if empty else [claim], list(claim))
            with patch.multiple(chain, REPO_ROOT=root, CHAIN=root / "chain.json",
                                LEDGER=root / "ledger.jsonl", REPORTS=reports,
                                CLAIMS=root / "claims.tsv", PRIVATE_LEDGER=root / "absent.jsonl"), \
                    patch("sys.argv", ["validate_chain.py"]), contextlib.redirect_stdout(io.StringIO()):
                try:
                    chain.main()
                except SystemExit as exc:
                    return exc.code
                return 0

    def test_valid_citation_passes(self):
        self.assertEqual(self.run_case("EV-0001"), 0)

    def test_blank_citations_are_rejected(self):
        for refs in ("", " ; \t ; "):
            self.assertEqual(self.run_case(refs), 1)

    def test_unknown_or_malformed_citation_is_rejected(self):
        for refs in ("EV-9999", "0001"):
            self.assertEqual(self.run_case(refs), 1)

    def test_empty_manifest_is_rejected(self):
        self.assertEqual(self.run_case("EV-0001", empty=True), 1)


class RankingCheckTests(unittest.TestCase):
    def test_check_only_accepts_match_and_rejects_drift_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row = dict(drug_name="synthetic compound", axis="synthetic axis",
                       finalist_axis="yes", safety_direction_veto="no",
                       **{field: "1" for field in ranking.SCORE_FIELDS},
                       ev_refs="EV-0001", rationale="Synthetic fixture only")
            write_tsv(root / "scores.tsv", [row])
            write_tsv(root / "pool.tsv", [dict(drug_name=row["drug_name"], us_status="us_approved")])
            write_tsv(root / "products.tsv", [dict(
                drug_name=row["drug_name"], product_class="approved_direct_product",
                retrieved_at=date.today().isoformat())])
            output = root / "ranked.tsv"
            with patch.multiple(ranking, INPUT=root / "scores.tsv", POOL=root / "pool.tsv",
                                PRODUCTS=root / "products.tsv", OUT=output), \
                    patch.object(ranking, "load_evidence", return_value={
                        "EV-0001": {"verification_status": "verified"}}), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(ranking.main(["--check-only"]), 1)
                self.assertFalse(output.exists())
                self.assertEqual(ranking.main([]), 0)
                baseline = output.read_bytes()
                timestamp = output.stat().st_mtime_ns
                self.assertEqual(ranking.main(["--check-only"]), 0)
                self.assertEqual(output.read_bytes(), baseline)
                self.assertEqual(output.stat().st_mtime_ns, timestamp)
                row["testability"] = "2"
                write_tsv(root / "scores.tsv", [row])
                self.assertEqual(ranking.main(["--check-only"]), 1)
                self.assertEqual(output.read_bytes(), baseline)
                self.assertEqual(output.stat().st_mtime_ns, timestamp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
