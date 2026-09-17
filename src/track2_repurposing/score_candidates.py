#!/usr/bin/env python3
"""Traceable research-priority ranking; never an efficacy or treatment score."""
from __future__ import annotations
import argparse, csv, io, json, sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INPUT = REPO / "research/drug_priority_scores.tsv"
LEDGER = REPO / "research/evidence.jsonl"
PRIVATE_LEDGER = REPO / "data/processed/evidence_private.jsonl"
POOL = REPO / "data/processed/track2/drug_pool.tsv"
PRODUCTS = REPO / "research/drug_product_status.tsv"
OUT = REPO / "data/processed/track2/candidates_ranked.tsv"
BASE_WEIGHTS = {"disease_model_evidence": 3, "mechanism_target_engagement": 3,
                "testability": 2, "human_exposure_precedent": 1,
                "pediatric_chronic_feasibility": 1, "translation_distance": -2,
                "counter_evidence_severity": -2}
SCENARIOS = {
    "base": BASE_WEIGHTS,
    "rigor_heavy": {**BASE_WEIGHTS, "disease_model_evidence": 4,
                    "mechanism_target_engagement": 4, "translation_distance": -3},
    "feasibility_heavy": {**BASE_WEIGHTS, "testability": 3,
                          "pediatric_chronic_feasibility": 2},
    "no_human_precedent": {**BASE_WEIGHTS, "human_exposure_precedent": 0},
    "counter_heavy": {**BASE_WEIGHTS, "counter_evidence_severity": -3},
}
SCORE_FIELDS = tuple(BASE_WEIGHTS)

def load_evidence():
    out = {}
    for path in (LEDGER, PRIVATE_LEDGER):
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    entry = json.loads(line); out[entry["id"]] = entry
    return out

def score(row, weights):
    return sum(int(row[field]) * weights[field] for field in SCORE_FIELDS)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true",
                        help="Compare the saved ranking with current inputs without writing outputs")
    args = parser.parse_args(argv)
    if not POOL.exists():
        sys.exit(f"missing {POOL}; run build_drug_pool.py first")
    evidence = load_evidence()
    with open(POOL) as handle:
        pool = {r["drug_name"]: r for r in csv.DictReader(handle, delimiter="\t")}
    with open(INPUT) as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    with open(PRODUCTS) as handle:
        products = {r["drug_name"]: r for r in csv.DictReader(handle, delimiter="\t")}
    errors = []
    for row in rows:
        name = row["drug_name"]
        if pool.get(name, {}).get("us_status") != "us_approved":
            errors.append(f"{name}: no us_approved pool record")
        if name not in products:
            errors.append(f"{name}: no product-level status record")
        else:
            age = (date.today() - date.fromisoformat(products[name]["retrieved_at"])).days
            if age > 30: errors.append(f"{name}: product evidence is stale ({age} days)")
        if row.get("finalist_axis") not in {"yes", "no"} or row.get("safety_direction_veto") not in {"yes", "no"}:
            errors.append(f"{name}: invalid finalist_axis or safety_direction_veto")
        for field in SCORE_FIELDS:
            try: value = int(row[field])
            except ValueError:
                errors.append(f"{name}: {field} is not an integer"); continue
            if not 0 <= value <= 3: errors.append(f"{name}: {field}={value} outside 0..3")
        refs = [x for x in row["ev_refs"].split(";") if x]
        if not refs: errors.append(f"{name}: no EV references")
        for ref in refs:
            entry = evidence.get(ref)
            if entry is None: errors.append(f"{name}: missing {ref}")
            elif entry.get("verification_status") != "verified":
                errors.append(f"{name}: {ref} is not verified")
    if errors:
        print("research-priority validation failed:", file=sys.stderr)
        for error in errors: print(f"  - {error}", file=sys.stderr)
        return 1
    ranks, scores = {}, {}
    for scenario, weights in SCENARIOS.items():
        ordered = sorted(rows, key=lambda r: (-score(r, weights), r["drug_name"]))
        ranks[scenario] = {r["drug_name"]: i for i, r in enumerate(ordered, 1)}
        scores[scenario] = {r["drug_name"]: score(r, weights) for r in rows}
    rows.sort(key=lambda r: (ranks["base"][r["drug_name"]], r["drug_name"]))
    selected_axes = set()
    selection = {}
    for row in rows:
        name, axis = row["drug_name"], row["axis"]
        direct = products[name]["product_class"] == "approved_direct_product"
        if row["safety_direction_veto"] == "yes": status, reason = "excluded_high_risk", "safety/direction hard veto"
        elif not direct: status, reason = "conditional", "no matching direct marketed product verified"
        elif row["finalist_axis"] != "yes": status, reason = "alternate", "predeclared same-axis alternate"
        elif axis in selected_axes: status, reason = "alternate", "higher-ranked eligible candidate already represents axis"
        else:
            status, reason = "finalist", "highest-ranked eligible predeclared independent axis"
            selected_axes.add(axis)
        selection[name] = (status, reason)
    fields = ["drug", "axis", "research_priority_score", "rank_min", "rank_max",
              *SCORE_FIELDS, "us_status", "product_class", "product_eligible",
              "selection_status", "selection_reason", "ev_refs", "rationale"]
    with io.StringIO(newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t"); writer.writeheader()
        for row in rows:
            name = row["drug_name"]; rr = [value[name] for value in ranks.values()]
            writer.writerow({"drug": name, "axis": row["axis"],
                "research_priority_score": scores["base"][name], "rank_min": min(rr),
                "rank_max": max(rr), **{f: row[f] for f in SCORE_FIELDS},
                "us_status": pool[name]["us_status"],
                "product_class": products[name]["product_class"],
                "product_eligible": "yes" if products[name]["product_class"] == "approved_direct_product" else "no",
                "selection_status": selection[name][0], "selection_reason": selection[name][1],
                "ev_refs": row["ev_refs"],
                "rationale": row["rationale"]})
        rendered = handle.getvalue()
    if args.check_only:
        if not OUT.is_file():
            print(f"FAIL saved ranking missing: {OUT}", file=sys.stderr)
            return 1
        with OUT.open(newline="") as handle:
            saved = csv.DictReader(handle, delimiter="\t")
            saved_rows = list(saved)
            saved_fields = saved.fieldnames
        expected_rows = list(csv.DictReader(io.StringIO(rendered), delimiter="\t"))
        if saved_fields != fields or saved_rows != expected_rows:
            print("FAIL saved ranking differs from current inputs; no files changed", file=sys.stderr)
            return 1
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(rendered)
    for row in rows:
        name = row["drug_name"]; rr = [value[name] for value in ranks.values()]
        print(f"{name:32} priority={scores['base'][name]:>3} rank={ranks['base'][name]} sensitivity={min(rr)}-{max(rr)} {selection[name][0]}")
    print(f"{'verified existing output (read-only)' if args.check_only else 'output'}: {OUT}\n"
          "Research-priority ranking only; not efficacy or treatment advice.")
    return 0

if __name__ == "__main__": raise SystemExit(main())
