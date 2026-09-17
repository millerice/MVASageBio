#!/usr/bin/env python3
"""Read saved L002 input metadata only; never execute the runner or hash raw inputs.

Print allowlisted categories, not filenames, paths, commands or genomic values.
Missing records are unverified, not an experimental failure.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

PINNED_RUNNER = "d041272d7a1faf8cd1797a5565cdf17ad7bccd2947006b4dcb4e5d53a3222b04"
LIMIT = 2 * 1024 * 1024


def read_small(path):
    try:
        with path.open("rb") as handle:
            value = handle.read(LIMIT + 1)
        if len(value) > LIMIT:
            return None, "too_large_not_inspected"
        return value, "read"
    except OSError:
        return None, "missing_or_unreadable"


def expected_inputs(source):
    # Only parse the known, hash-pinned runner. No shell evaluation.
    values = {"ROOT": "/placeholder"}
    for name in ("REF", "TARGETS", "VALIDATOR", "PREFIX", "R1", "R2"):
        match = re.search(r"^" + name + r"=(\S+)$", source, re.M)
        if not match:
            raise ValueError("unsupported assignment")
        def substitute(m):
            return values[m[1] or m[2]]
        values[name] = re.sub(r"\$\{(\w+)\}|\$(\w+)", substitute, match[1])
    result = {}
    for variable, label in (("VALIDATOR", "validator"), ("REF", "reference"),
                            ("TARGETS", "targets"), ("R1", "fastq_R1"), ("R2", "fastq_R2")):
        matches = re.findall(r'^check_hash "\$' + variable + r'" ([0-9a-f]{64})$', source, re.M)
        if len(matches) != 1:
            raise ValueError("unsupported checksum declaration")
        result[Path(values[variable]).name] = (label, matches[0])
    if len(result) != 5:
        raise ValueError("ambiguous names")
    return result


def compare_manifest(text, expected):
    found, malformed = {}, False
    for line in text.splitlines():
        m = re.fullmatch(r"([0-9a-fA-F]{64}) [ *]([^/\\]+)", line)
        if not m or m[2] not in expected or m[2] in found:
            malformed = True
            continue
        found[m[2]] = m[1].lower()
    return {
        "exact_expected_entries": not malformed and set(found) == set(expected),
        "saved_digest_matches_runner_expectation": {
            label: found[name] == digest if name in found else None
            for name, (label, digest) in expected.items()
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("/home/mva_q2"))
    parser.add_argument("--l002-run", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"q1_l002_[A-Za-z0-9_]+", args.l002_run):
        parser.error("Expected an existing q1_l002_ run basename")
    run = args.root / "out" / args.l002_run
    report = {
        "analysis": "read_only_saved_input_metadata",
        "collector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "raw_inputs_read": False,
    }
    runner, status = read_small(args.root / "q1_l002_extension/run.sh")
    pinned = runner is not None and hashlib.sha256(runner).hexdigest() == PINNED_RUNNER
    report["runner"] = {"status": status, "matches_previously_checked_runner": pinned}
    manifest, status = read_small(run / "private/input_checksums.sha256")
    report["saved_input_manifest"] = {"status": status}
    if pinned and manifest is not None:
        try:
            report["saved_input_manifest"].update(compare_manifest(
                manifest.decode("utf-8"), expected_inputs(runner.decode("utf-8"))))
        except (UnicodeError, ValueError, KeyError):
            report["saved_input_manifest"]["comparison"] = "unsupported_format_not_compared"
    else:
        report["saved_input_manifest"]["comparison"] = "not_compared"
    log, status = read_small(run / "logs/minimap2.log")
    report["alignment_log"] = {"status": status}
    if log is not None:
        # These markers are supporting metadata, not an exit-code certificate.
        report["alignment_log"].update({
            "command_marker_present": bool(re.search(rb"(?m)^\[M::main\] CMD:", log)),
            "timing_marker_present": bool(re.search(rb"(?m)^\[M::main\] Real time:", log)),
        })
    report["other_records_present"] = {
        "duplicate_stats": (run / "logs/markdup_stats.txt").is_file(),
        "saved_code_manifest": (run / "private/code_checksums.sha256").is_file(),
        "safe_summary": (run / "return/q1_l002_safe_summary.json").is_file(),
        "return_checksums": (run / "return/RETURN_CHECKSUMS.sha256").is_file(),
    }
    report["limitations"] = [
        "Saved digests are compared with expectations in the pinned runner, not with current input bytes.",
        "The origin of the runner's expected digests is not independently verified here.",
        "Log markers and file presence do not prove successful execution or code/input/output binding.",
        "No BAM body, FASTQ, reference sequence, target contents or shell history is read.",
        "This stage does not investigate Q2 packaging history or establish a scientific pass/fail verdict.",
    ]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
