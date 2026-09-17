#!/usr/bin/env python3
"""Calibrate chromosome-depth sensitivity with pre-correction spike-ins.

This script is public and contains no patient coordinates or measurements. Inputs and
outputs belong in gitignored ``data/processed``. It injects chromosome-wide copy-depth
effects before repeating the GC-decile correction, then uses a 1-Mb block bootstrap to
retain local depth correlation.

The result measures recovery of additional multiplicative gains relative to the
observed sample. The legacy output names "null" and "detection_power" refer to that
empirical baseline, not a calibrated biological no-gain null or an exclusion bound.
It cannot test random cell-to-cell MVA karyotypes or tissue-restricted mosaicism.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

AUTOS = tuple(str(i) for i in range(1, 23))


def percentile(values: list[float], q: float) -> float:
    values = sorted(values)
    if not values:
        return float("nan")
    x = (len(values) - 1) * q
    lo, hi = math.floor(x), math.ceil(x)
    if lo == hi:
        return values[lo]
    return values[lo] * (hi - x) + values[hi] * (x - lo)


def load_bins(regions: Path, gc_bins: Path, blacklist: Path, bin_size: int) -> list[dict]:
    rows: dict[tuple[str, int], dict] = {}
    opener = gzip.open if regions.suffix == ".gz" else open
    with opener(regions, "rt") as handle:
        for line in handle:
            chrom, start, end, depth = line.split()[:4]
            if chrom in AUTOS:
                rows[(chrom, int(start))] = {
                    "chrom": chrom, "start": int(start), "end": int(end),
                    "depth": float(depth),
                }

    with open(gc_bins, encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            chrom, start, _end, gc, n_frac = line.split()[:5]
            key = (chrom, int(start))
            if key in rows:
                rows[key]["gc"] = float(gc)
                rows[key]["n_frac"] = float(n_frac)

    overlap: dict[tuple[str, int], int] = defaultdict(int)
    with open(blacklist, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(("#", "track", "browser")):
                continue
            fields = line.split()
            chrom = fields[0][3:] if fields[0].startswith("chr") else fields[0]
            if chrom not in AUTOS:
                continue
            start, end = int(fields[1]), int(fields[2])
            for bin_start in range((start // bin_size) * bin_size, end, bin_size):
                key = (chrom, bin_start)
                if key in rows:
                    overlap[key] += max(0, min(end, rows[key]["end"]) - max(start, bin_start))

    kept = []
    for key, row in rows.items():
        missing = "gc" not in row or "n_frac" not in row
        black_frac = overlap[key] / (row["end"] - row["start"])
        if not missing and row["n_frac"] < 0.05 and black_frac < 0.5:
            row["block"] = row["start"] // 1_000_000
            kept.append(row)
    if not kept:
        raise ValueError("no usable autosomal bins after masking")
    return kept


def corrected_deviation(rows: list[dict], target: str, effect: float) -> float:
    # Callers keep rows GC-sorted. Sorting once per bootstrap, rather than once per
    # target/effect, cuts calibration time by roughly an order of magnitude.
    ordered = rows
    n = len(ordered)
    expected: list[float] = []
    groups: list[list[dict]] = []
    for decile in range(10):
        group = ordered[decile * n // 10:(decile + 1) * n // 10]
        groups.append(group)
        expected.append(st.median(r["depth"] * (1 + effect if r["chrom"] == target else 1)
                                  for r in group))
    ratios: dict[str, list[float]] = defaultdict(list)
    for decile, group in enumerate(groups):
        for row in group:
            depth = row["depth"] * (1 + effect if row["chrom"] == target else 1)
            ratios[row["chrom"]].append(depth / expected[decile])
    baseline = st.median(x for chrom in AUTOS for x in ratios[chrom])
    return st.median(ratios[target]) / baseline - 1


def block_bootstrap(rows: list[dict], rng: random.Random) -> list[dict]:
    by_chrom_block: dict[str, dict[int, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        by_chrom_block[row["chrom"]][row["block"]].append(row)
    sample: list[dict] = []
    for chrom in AUTOS:
        blocks = list(by_chrom_block[chrom].values())
        for _ in range(len(blocks)):
            sample.extend(rng.choice(blocks))
    return sorted(sample, key=lambda r: (r["gc"], r["chrom"], r["start"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--regions", type=Path, required=True)
    parser.add_argument("--gc-bins", type=Path, required=True)
    parser.add_argument("--blacklist", type=Path, required=True)
    parser.add_argument("--targets", default="20,21,22")
    parser.add_argument("--effects", default="0.025,0.05,0.075,0.10,0.125,0.15")
    parser.add_argument("--replicates", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260915)
    parser.add_argument("--bin-size", type=int, default=100_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.replicates < 100:
        parser.error("--replicates must be at least 100")

    targets = [x.strip() for x in args.targets.split(",") if x.strip()]
    effects = [float(x) for x in args.effects.split(",")]
    if any(t not in AUTOS for t in targets) or any(e <= 0 for e in effects):
        parser.error("targets must be autosomes and effects must be positive")

    rows = sorted(load_bins(args.regions, args.gc_bins, args.blacklist, args.bin_size),
                  key=lambda r: (r["gc"], r["chrom"], r["start"]))
    rng = random.Random(args.seed)
    bootstraps = [block_bootstrap(rows, rng) for _ in range(args.replicates)]
    result = {
        "scope": "stable whole-chromosome gain in the assayed bulk tissue only",
        "limitations": [
            "does not test random cell-to-cell variegated karyotypes",
            "does not test tissue-restricted mosaicism",
            "simulation models multiplicative chromosome-wide depth gains",
            "idealized trisomic-cell equivalents assume equal DNA contribution from diploid and complete-trisomy cells",
        ],
        "method": "1-Mb block bootstrap; spike-in before GC-decile correction",
        "replicates": args.replicates,
        "seed": args.seed,
        "n_bins": len(rows),
        "targets": {},
    }
    for target in targets:
        # Preserve historical output keys and calculations. "null" resamples the
        # observed sample; it does not remove pre-existing signal or systematic bias.
        null = [corrected_deviation(sample, target, 0.0) for sample in bootstraps]
        observed = corrected_deviation(rows, target, 0.0)
        threshold = percentile(null, 0.95)
        entry = {
            "observed_deviation": observed,
            "observed_bootstrap_ci95": [percentile(null, 0.025), percentile(null, 0.975)],
            "one_sided_null_threshold_95": threshold,
            "effects": {},
        }
        for effect in effects:
            sims = [corrected_deviation(sample, target, effect) for sample in bootstraps]
            paired_recovery = [(((1 + sim) / (1 + base)) - 1) / effect
                               for sim, base in zip(sims, null)]
            entry["effects"][str(effect)] = {
                "idealized_trisomic_cell_fraction_equivalent": 2 * effect,
                "median_recovered_deviation": st.median(sims),
                "paired_incremental_recovery_fraction": st.median(paired_recovery),
                "simulation_ci95": [percentile(sims, 0.025), percentile(sims, 0.975)],
                "detection_power": sum(x > threshold for x in sims) / len(sims),
                "separated_from_observed_null_at_95pct": percentile(sims, 0.025) > percentile(null, 0.975),
            }
        result["targets"][target] = entry

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"calibration written to {args.output} ({args.replicates} replicates)")
    for target, entry in result["targets"].items():
        print(f"chr{target}: observed={entry['observed_deviation']:+.3%}, "
              f"bootstrap CI={entry['observed_bootstrap_ci95'][0]:+.3%}.."
              f"{entry['observed_bootstrap_ci95'][1]:+.3%}")
        for effect, values in entry["effects"].items():
            print(f"  spike {float(effect):.1%}: recovered={values['median_recovered_deviation']:+.3%}, "
                  f"paired_recovery={values['paired_incremental_recovery_fraction']:.1%}, "
                  f"power={values['detection_power']:.1%}, "
                  f"separated={values['separated_from_observed_null_at_95pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
