#!/usr/bin/env python3
"""Quality-filtered query-name-deduplicated support check for private SNV targets."""
from __future__ import annotations
import argparse, csv, json, re, subprocess
from collections import Counter
from pathlib import Path

CIGAR_RE = re.compile(r"(\d+)([MIDNSHP=X])")

def base_at(pos: int, pos0: int, cigar: str, seq: str, qual: str):
    ref_pos, query_pos = pos0 - 1, 0
    for size, op in CIGAR_RE.findall(cigar):
        size = int(size)
        if op in "M=X":
            if ref_pos <= pos - 1 < ref_pos + size:
                offset = pos - 1 - ref_pos
                return seq[query_pos + offset], ord(qual[query_pos + offset]) - 33
            ref_pos += size; query_pos += size
        elif op in "DN":
            if ref_pos <= pos - 1 < ref_pos + size: return None
            ref_pos += size
        elif op in "IS": query_pos += size
    return None

def validate_target(bam: Path, target: dict[str, str], mapq_min: int, bq_min: int):
    pos = int(target["position"])
    region = f"{target['contig']}:{pos - 100}-{pos + 100}"
    fragments: dict[str, tuple[str, int]] = {}
    conflicts = 0
    proc = subprocess.Popen(["samtools", "view", str(bam), region], stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        fields = line.rstrip("\n").split("\t")
        flag, mapq = int(fields[1]), int(fields[4])
        if flag & (0x4 | 0x100 | 0x800) or mapq < mapq_min: continue
        observed = base_at(pos, int(fields[3]), fields[5], fields[9], fields[10])
        if observed is None or observed[1] < bq_min: continue
        base, bq = observed
        allele = "REF" if base.upper() == target["ref"].upper() else ("ALT" if base.upper() == target["alt"].upper() else "OTHER")
        old = fragments.get(fields[0])
        if old is not None:
            conflicts += old[0] != allele
            if bq > old[1]: fragments[fields[0]] = (allele, bq)
        else: fragments[fields[0]] = (allele, bq)
    if proc.wait() != 0: raise RuntimeError(f"samtools view failed for target {target['label']}")
    counts = Counter(allele for allele, _ in fragments.values())
    usable = counts["REF"] + counts["ALT"]
    fraction = counts["ALT"] / usable if usable else 0.0
    # The pre-registered Q1 criterion includes no contradictory mate observation.
    passed = counts["ALT"] >= 5 and 0.30 <= fraction <= 0.70 and conflicts == 0
    return set(fragments), {**target, "ref_fragments": counts["REF"], "alt_fragments": counts["ALT"], "other_fragments": counts["OTHER"], "usable_fragments": usable, "alt_fraction": f"{fraction:.6f}", "mate_conflicts": conflicts, "read_support_pass": str(passed).lower()}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bam", required=True, type=Path); ap.add_argument("--targets", required=True, type=Path)
    ap.add_argument("--private-detail", required=True, type=Path); ap.add_argument("--safe-summary", required=True, type=Path)
    ap.add_argument("--mapq-min", default=20, type=int); ap.add_argument("--baseq-min", default=20, type=int)
    args = ap.parse_args()
    with args.targets.open() as handle: targets = list(csv.DictReader(handle, delimiter="\t"))
    required = {"label", "contig", "position", "ref", "alt"}
    if len(targets) != 2 or not targets or set(targets[0]) != required: raise SystemExit("targets must contain exactly two rows and five required columns")
    if any(len(t["ref"]) != 1 or len(t["alt"]) != 1 for t in targets): raise SystemExit("this task supports SNVs only")
    names, details = zip(*(validate_target(args.bam, t, args.mapq_min, args.baseq_min) for t in targets))
    phase_status = "molecule_overlap_observed_requires_private_review" if names[0] & names[1] else "not_establishable_short_read_geometry"
    args.private_detail.parent.mkdir(parents=True, exist_ok=True)
    with args.private_detail.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=details[0].keys(), delimiter="\t"); writer.writeheader(); writer.writerows(details)
    safe = {"schema_version": 2, "analysis": "full_reference_query_name_deduplicated_read_support", "quality_filters": {"mapq_min": args.mapq_min, "baseq_min": args.baseq_min}, "candidates": [{"label": d["label"], "read_support_status": "pass" if d["read_support_pass"] == "true" else "not_pass"} for d in details], "direct_phase_status": phase_status}
    args.safe_summary.parent.mkdir(parents=True, exist_ok=True); args.safe_summary.write_text(json.dumps(safe, indent=2) + "\n")

if __name__ == "__main__": main()
