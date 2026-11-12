#!/usr/bin/env python3
"""Unified public preflight. Existing project outputs are read-only; tests use temp files."""
from __future__ import annotations
import hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENOMIC_SUFFIXES = (".vcf", ".vcf.gz", ".bam", ".cram", ".fastq", ".fastq.gz", ".fq", ".fq.gz")
REPORT_LEAK_PATTERNS = {
    "transcript accession": re.compile(r"\bNM_\d+"),
    "coding HGVS": re.compile(r"\bc\.\d+[A-Za-z0-9_+*=>-]*"),
    "protein HGVS": re.compile(r"\bp\.[A-Z][a-z]{2}\d+"),
    "single-letter protein variant": re.compile(r"\b[A-Z]\d{2,5}[A-Z*]\b"),
    "non-coding/genomic HGVS": re.compile(r"\b[gmn]\.\d+[A-Za-z0-9_+*=>-]*"),
    "genomic coordinate": re.compile(r"\bchr(?:[1-9]|1\d|2[0-2]|X|Y):\d+"),
    "allele-depth value": re.compile(r"\b(?:AD|BAF)\s*(?:=|\(|:)\s*\d", re.I),
    "patient ALT count": re.compile(r"(?:≥|>=)\s*\d+[^\n]{0,30}\bALT", re.I),
    "patient ALT count reversed": re.compile(r"\bALT[^\n]{0,30}(?:=|:)\s*\d+", re.I),
}
# Applied to every blob reachable from HEAD: a push publishes history, not just the working tree.
# Patterns are narrower than REPORT_LEAK_PATTERNS so official template examples and gnomAD
# region ranges in the ledger do not trip them.
HISTORY_LEAK_PATTERNS = {
    "coding HGVS": re.compile(rb"\bc\.\d+(?:[+-]\d+)?(?:[ACGT]>[ACGT]|del|dup|ins)"),
    "protein HGVS": re.compile(rb"\bp\.\(?[A-Z][a-z]{2}\d+(?:[A-Z][a-z]{2}|Ter|\*|fs)"),
    "transcript accession": re.compile(rb"\bNM_\d{6}\.\d+"),
    "coordinate with alleles": re.compile(
        rb"\bchr(?:[1-9]|1\d|2[0-2]|X|Y)[:\t ,]\d{7,}[\t ,:]*[ACGT]+\s*(?:>|,)\s*[ACGT]+"),
    "T1 data row": re.compile(rb"PROBAND01,chr\w+,\d{7,}"),
}

def history_leaks(repo, rev="HEAD"):
    """Return sorted (path, label) pairs for leak patterns in any blob reachable from rev."""
    listing = subprocess.run(["git", "rev-list", "--objects", rev], cwd=repo,
                             capture_output=True, text=True, check=True).stdout.splitlines()
    paths = {}
    for line in listing:
        sha, _, path = line.partition(" ")
        if path:
            paths.setdefault(sha, path)
    found = set()
    messages = subprocess.run(["git", "log", "--format=%h%x00%B%x01", rev], cwd=repo,
                              capture_output=True, check=True).stdout
    for record in messages.split(b"\x01"):
        commit, _, body = record.strip().partition(b"\x00")
        found.update((f"commit message {commit.decode()}", label)
                     for label, pattern in HISTORY_LEAK_PATTERNS.items() if pattern.search(body))
    if not paths:
        return sorted(found)
    batch = subprocess.run(["git", "cat-file", "--batch"], cwd=repo, capture_output=True, check=True,
                           input="".join(f"{sha}\n" for sha in paths).encode()).stdout
    offset = 0
    for sha, path in paths.items():
        header_end = batch.index(b"\n", offset)
        _, kind, size = batch[offset:header_end].split()
        start = header_end + 1
        offset = start + int(size) + 1
        if kind != b"blob":
            continue
        blob = batch[start:start + int(size)]
        found.update((path, label) for label, pattern in HISTORY_LEAK_PATTERNS.items() if pattern.search(blob))
    return sorted(found)

def run(label, command):
    print(f"\n== {label} ==")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode

def main():
    final = "--final" in sys.argv[1:]
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    leaked = [p for p in tracked if p.startswith(("data/raw/", "data/processed/")) or p.endswith(GENOMIC_SUFFIXES)]
    if leaked:
        print("FAIL genomic/private paths tracked by git:")
        for path in leaked: print(f"  - {path}")
        return 1
    public_text = list((ROOT / "reports").glob("*.md"))
    public_text += list((ROOT / "submissions").glob("**/*.md"))
    public_text += [ROOT / "README.md"]
    for report in public_text:
        content = report.read_text(encoding="utf-8")
        for label, pattern in REPORT_LEAK_PATTERNS.items():
            match = pattern.search(content)
            if match:
                print(f"FAIL public-report leak ({label}) in {report.relative_to(ROOT)}: {match.group(0)!r}")
                return 1
    if shutil.which("pdftotext"):
        for pdf in (ROOT / "reports").glob("*.pdf"):
            extracted = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True)
            if extracted.returncode != 0:
                print(f"FAIL could not inspect public PDF {pdf.relative_to(ROOT)}")
                return 1
            for label, pattern in REPORT_LEAK_PATTERNS.items():
                if pattern.search(extracted.stdout):
                    print(f"FAIL public-PDF leak ({label}) in {pdf.relative_to(ROOT)}")
                    return 1
    history = history_leaks(ROOT)
    if history:
        print("FAIL variant-level pattern in git history reachable from HEAD (rewrite before pushing):")
        for path, label in history: print(f"  - {path}: {label}")
        return 1
    checks = [
        ("public-history leak scan tests", [sys.executable, "src/common/test_validate_all.py"]),
        ("T1 scorer synthetic tests", [sys.executable, "src/track1_variant/test_scorer.py"]),
        ("Q2 power synthetic tests", [sys.executable, "src/track2_repurposing/test_depth_power.py"]),
        ("evidence ledger", [sys.executable, "src/track2_repurposing/ledger.py", "lint"]),
        ("mechanism, citations, claims", [sys.executable, "src/track2_repurposing/validate_chain.py"]),
        ("validation regression tests", [sys.executable, "src/track2_repurposing/test_validation.py"]),
        ("research-priority ranking", [sys.executable, "src/track2_repurposing/score_candidates.py", "--check-only"]),
        ("cross-review configuration", [sys.executable, "src/track2_repurposing/cross_review.py", "check"]),
    ]
    failures = sum(run(label, [command[0], "-B", *command[1:]]) != 0 for label, command in checks)
    if final:
        import csv
        with open(ROOT / "research/report_claims.tsv", encoding="utf-8") as handle:
            claim_rows = list(csv.DictReader(handle, delimiter="\t"))
            all_claims = [r["claim_id"] for r in claim_rows]
            pending = [r["claim_id"] for r in claim_rows if r["review_status"] != "independent_reviewed"]
        if pending:
            print(f"\nFAIL final gate: claims pending independent review: {', '.join(pending)}")
            failures += 1
        attestations = ROOT / "research/review_attestations.jsonl"
        report = ROOT / "reports/JiuTian-Bio_track2_report.md"
        digest = hashlib.sha256(report.read_bytes()).hexdigest()
        reviewed = set()
        if attestations.exists():
            for line in attestations.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    item = json.loads(line)
                    if item.get("report_sha256") == digest and item.get("status") == "passed":
                        reviewed.update(item.get("claim_ids", []))
        missing_review = [cid for cid in all_claims if cid not in reviewed]
        if missing_review:
            print(f"FAIL final gate: no hash-bound independent attestation for: {', '.join(missing_review)}")
            failures += 1
    print(f"\n{'PASS' if not failures else 'FAIL'} unified preflight ({failures} failing gate(s))")
    return 1 if failures else 0

if __name__ == "__main__": raise SystemExit(main())
