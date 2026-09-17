#!/usr/bin/env python3
"""Apply the frozen Q1 validator to four BAMs; export categorical results only."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path


def category(d):
    ref, alt = int(d['ref_fragments']), int(d['alt_fragments'])
    total = ref + alt
    reasons = []
    if total == 0:
        reasons.append('NO_USABLE_REF_ALT_SUPPORT')
    if alt < 5:
        reasons.append('ALT_SUPPORT_BELOW_THRESHOLD')
    if total and not 3 * total <= 10 * alt <= 7 * total:
        reasons.append('ALLELE_BALANCE_OUTSIDE_RANGE')
    original_pass = not reasons
    if int(d['mate_conflicts']):
        reasons.append('MATE_CONFLICT_PRESENT')
    return {
        'original_support_threshold_pass': original_pass,
        'extended_support_status': 'not_pass' if reasons else 'pass',
        'reason_categories': reasons,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--validator', required=True, type=Path)
    ap.add_argument('--targets', required=True, type=Path)
    ap.add_argument('--reference', required=True, type=Path)
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--l001-before', type=Path)
    ap.add_argument('--l001-after', type=Path)
    ap.add_argument('--l002-before', type=Path)
    ap.add_argument('--l002-after', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    import subprocess
    with args.targets.open() as f:
        targets = list(csv.DictReader(f, delimiter='\t'))
    required = {'label', 'contig', 'position', 'ref', 'alt'}
    if len(targets) != 2 or any(set(t) != required for t in targets):
        raise SystemExit('Invalid private target schema')
    if len({(t['contig'], t['position']) for t in targets}) != 2:
        raise SystemExit('Targets must be distinct')
    for t in targets:
        if t['ref'].upper() not in 'ACGT' or t['alt'].upper() not in 'ACGT' or len(t['ref']) != 1 or len(t['alt']) != 1 or t['ref'].upper() == t['alt'].upper() or int(t['position']) < 101:
            raise SystemExit('Unsupported private SNV target')
        region = '{}:{}-{}'.format(t['contig'], t['position'], t['position'])
        p = subprocess.run(['samtools', 'faidx', str(args.reference), region], capture_output=True, text=True)
        base = ''.join(x for x in p.stdout.splitlines() if not x.startswith('>'))
        if p.returncode or base.upper() != t['ref'].upper():
            raise SystemExit('Private target/reference consistency failed')
    if args.check_only:
        print('PRIVATE_TARGET_REFERENCE_PASS')
        return
    spec = importlib.util.spec_from_file_location('frozen_q1', args.validator)
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    stages = {
        'L001_before': args.l001_before, 'L001_after': args.l001_after,
        'L002_before': args.l002_before, 'L002_after': args.l002_after,
    }
    if args.output is None or any(p is None or not p.is_file() for p in stages.values()):
        raise SystemExit('All four BAMs and an output directory are required')
    private, safe = {}, {}
    for stage, bam in stages.items():
        observations = [validator.validate_target(bam, t, 20, 20) for t in targets]
        details = [v[1] for v in observations]
        private[stage] = details
        safe[stage] = {
            'candidates': [dict(candidate='candidate_{}'.format(i + 1), **category(d)) for i, d in enumerate(details)],
            'direct_phase_status': 'overlap_requires_private_review' if observations[0][0] & observations[1][0] else 'not_established_no_shared_qualified_query_name',
        }
    (args.output / 'private').mkdir(exist_ok=True)
    (args.output / 'return').mkdir(exist_ok=True)
    (args.output / 'private/details.json').write_text(json.dumps(private, indent=2) + '\n')
    result = {
        'schema_version': 1, 'analysis': 'L002_standalone_with_L001_baseline',
        'quality_filters': {'mapq_min': 20, 'baseq_min': 20},
        'method': 'Frozen Q1 validator; mate-conflict veto is an added criterion, not the original preregistration.',
        'library_relationship': 'unverified_no_joint_deduplication_performed',
        'phase_scope': 'Direct query-name overlap only; chained phasing has not been assessed.',
        'stages': safe,
    }
    (args.output / 'return/q1_l002_safe_summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print('CATEGORICAL_SUMMARY_COMPLETE')


if __name__ == '__main__':
    main()
