#!/usr/bin/env python3
"""Read existing code/manifest and BAM headers; print categorical provenance metadata.

No files are written. No FASTQ, target TSV, alignments, or private counts are read.
Current hashes and saved headers do not by themselves prove historical execution.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


def digest(path):
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def parse_header(text):
    references, programs = [], []
    for line in text.splitlines():
        parts = line.split("\t")
        tags = dict(p.split(":", 1) for p in parts[1:] if ":" in p)
        if parts[0] == "@SQ":
            references.append((tags.get("SN", ""), tags.get("LN", "")))
        if parts[0] == "@PG" and tags.get("PN") in {"minimap2", "samtools"}:
            version = tags.get("VN", "")
            programs.append({
                "program": tags["PN"],
                "version": version if re.fullmatch(r"[0-9][A-Za-z0-9.+_-]{0,63}", version)
                else "not_reported_or_not_exported",
            })
    # Never return CL commands, sample/read-group tags or sequence names in metadata.
    return references, {"header_programs": programs}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("/home/mva_q2"))
    ap.add_argument("--l002-run", required=True, help="Existing run directory basename under out/")
    args = ap.parse_args()
    if not re.fullmatch(r"q1_l002_[A-Za-z0-9_]+", args.l002_run):
        ap.error("Expected a q1_l002_ run basename")
    root = args.root
    run = root / "out" / args.l002_run
    scripts = {
        "q2_runner": root / "run_q2.sh",
        "q1_runner": root / "q1_full_reference_recheck/run_q1_full_reference.sh",
        "q1_validator": root / "q1_full_reference_recheck/validate_bam.py",
        "l002_runner": root / "q1_l002_extension/run.sh",
        "l002_summary": root / "q1_l002_extension/summarize.py",
    }
    hashes = {label: digest(path) for label, path in scripts.items()}
    report = {
        "analysis": "read_only_provenance_metadata",
        "collector_sha256": digest(Path(__file__)),
        "current_code_sha256": hashes,
        "missing_hash_means": "expected_location_missing_or_unreadable",
        "scope": "Current code and saved metadata only; historical execution and FASTQ identity remain unproven.",
    }
    manifest = run / "private/code_checksums.sha256"
    wanted = {scripts[k].name: k for k in ("q1_validator", "l002_runner", "l002_summary")}
    matches = {}
    manifest_valid = True
    try:
        for line in manifest.read_text().splitlines():
            m = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](.+)", line)
            name = Path(m[2]).name if m else ""
            if not m or name not in wanted or wanted[name] in matches:
                manifest_valid = False
                continue
            label = wanted[name]
            matches[label] = {
                "saved_code_sha256": m[1].lower(),
                "matches_current_code": None if hashes[label] is None else hashes[label] == m[1].lower(),
            }
        manifest_valid = manifest_valid and set(matches) == set(wanted.values())
        report["l002_saved_code_manifest"] = {"status": "read", "expected_entries_valid": manifest_valid,
                                                "comparisons_by_basename_only": matches}
    except OSError:
        report["l002_saved_code_manifest"] = {"status": "missing_or_unreadable"}
    try:
        reference = []
        for line in (root / "ref/GRCh38.primary.fa.fai").read_text().splitlines():
            fields = line.split("\t")
            reference.append((fields[0], fields[1]))
    except (OSError, IndexError):
        reference = []
    bams = {
        "L001_before": root / "out/wg_l001.bam",
        "L001_after": root / "out/q1_full_reference/full.dedup.bam",
        "L002_before": run / "l002.before.bam",
        "L002_after": run / "l002.after.bam",
    }
    report["bam_headers"] = {}
    for label, bam in bams.items():
        status = report["bam_headers"][label] = {}
        if not bam.is_file():
            status["status"] = "missing_at_expected_location"
            continue
        if not shutil.which("samtools"):
            status["status"] = "samtools_unavailable"
            continue
        try:
            result = subprocess.run(["samtools", "view", "-H", str(bam)],
                                    capture_output=True, text=True, timeout=60)
            if result.returncode:
                status["status"] = "header_read_failed"
                continue
            sequences, metadata = parse_header(result.stdout)
            status.update(metadata)
            status["status"] = "header_read"
            status["names_lengths_match_current_reference_fai"] = (
                sequences == reference if sequences and reference else None)
        except (OSError, subprocess.TimeoutExpired):
            status["status"] = "header_read_failed_or_timed_out"
    report["limitations"] = [
        "No complete BAM hashing or body integrity check; only headers are inspected.",
        "Some samtools versions append a PG record while reading; not every exported program entry is historical.",
        "Reference-name/length agreement does not establish reference sequence identity.",
        "Saved manifest comparison uses expected code basenames; original paths are not exported or followed.",
        "Missing metadata is unverified, not a scientific failure; this script supplies no pass/fail verdict.",
    ]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
