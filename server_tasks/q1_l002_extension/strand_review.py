#!/usr/bin/env python3
"""Post-hoc orientation review; private counts and categorical export only."""
import argparse
import csv
import hashlib
import json
import math
import os
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


def fisher(table):
    a, b = table[0]
    c, d = table[1]
    r1, r2, col = a + b, c + d, a + c
    n = r1 + r2
    if not r1 or not r2 or not col or col == n:
        return None
    if n > 100000:
        raise ValueError('Unexpectedly large table')
    def choose(n, k):
        return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
    def probability(k):
        return choose(r1, k)+choose(r2, col-k)-choose(n, col)
    observed = probability(a)
    return min(1.0, math.fsum(math.exp(probability(k))
               for k in range(max(0, col-r2), min(r1, col)+1)
               if probability(k) <= observed + 1e-10))


def base_at(pos, start, cigar, seq, qual):
    r, q = start, 0
    for size, op in re.findall(r'(\d+)([MIDNSHP=X])', cigar):
        size = int(size)
        if op in 'M=X':
            if r <= pos < r+size:
                i = q+pos-r
                return seq[i].upper(), ord(qual[i])-33
            r += size
            q += size
        elif op in 'DN':
            if r <= pos < r+size:
                return None
            r += size
        elif op in 'IS':
            q += size
    return None


def analyze(lines, target):
    groups = defaultdict(list)
    for line in lines:
        f = line.rstrip().split('\t')
        flag = int(f[1])
        # Independent diagnostic filter: exclude QC-failed and marked duplicates too.
        if flag & (4 | 256 | 512 | 1024 | 2048) or int(f[4]) < 20:
            continue
        if f[9] == '*' or f[10] == '*':
            continue
        call = base_at(int(target['position']), int(f[3]), f[5], f[9], f[10])
        if call is None or call[1] < 20:
            continue
        allele = 'REF' if call[0] == target['ref'].upper() else 'ALT' if call[0] == target['alt'].upper() else 'OTHER'
        rg = next((v[5:] for v in f[11:] if v.startswith('RG:Z:')), '')
        groups[(rg, f[0])].append((allele, 'reverse' if flag & 16 else 'forward'))
    counts = Counter()
    for observations in groups.values():
        alleles = {x[0] for x in observations}
        if len(alleles) != 1:
            counts['conflicting_groups'] += 1
            continue
        allele = observations[0][0]
        if len(observations) > 1:
            # Do not arbitrarily pick a strand for overlapping mates or duplicate names.
            counts['multi_observation_groups'] += 1
            counts['multi_' + allele] += 1
            continue
        counts[allele + '_' + observations[0][1]] += 1
    table = [[counts['REF_forward'], counts['REF_reverse']],
             [counts['ALT_forward'], counts['ALT_reverse']]]
    p = fisher(table)
    orientation = 'BOTH_PRESENT' if all(table[1]) else 'FORWARD_ONLY' if table[1][0] else 'REVERSE_ONLY' if table[1][1] else 'NO_ALT_IN_SINGLE_OBSERVATION_SUBSET'
    safe = {
        'single_observation_alt_orientation': orientation,
        'multiple_qualified_observations_excluded': counts['multi_observation_groups'] > 0,
        'conflicting_groups_excluded': counts['conflicting_groups'] > 0,
        'other_alleles_present': any(v for k,v in counts.items() if 'OTHER' in k),
        'exploratory_fisher_category': 'NOT_ASSESSABLE' if p is None else 'NOMINAL_ASSOCIATION_DETECTED' if p < .05 else 'NO_NOMINAL_ASSOCIATION_DETECTED',
    }
    return {'counts': dict(counts), 'ref_alt_by_forward_reverse': table, 'fisher_two_sided_p': p}, safe


def selftest():
    assert abs(fisher([[1,9],[11,3]]) - .0027594561852200836) < 1e-10
    assert abs(fisher([[5,5],[5,5]]) - 1) < 1e-10
    assert fisher([[3,0],[2,0]]) is None
    target = dict(position='150', ref='A', alt='C')
    def row(name, flag, base):
        return '\t'.join(map(str,[name,flag,'synthetic',150,60,'1M','*',0,0,base,'I']))
    private, safe = analyze([row('overlap',65,'C'), row('overlap',145,'C'), row('conflict',65,'A'), row('conflict',145,'C'), row('single',0,'C')], target)
    assert private['ref_alt_by_forward_reverse'][1] == [1,0]
    assert safe['multiple_qualified_observations_excluded']
    assert safe['conflicting_groups_excluded']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path('/home/mva_q2'))
    ap.add_argument('--l002-run', default='q1_l002_20260916T154747Z_US5tTq')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    selftest()
    if args.self_test:
        print('SELF_TEST_PASS'); return
    root = args.root
    bams = {'L001_after': root/'out/q1_full_reference/full.dedup.bam',
            'L002_after': root/'out'/args.l002_run/'l002.after.bam'}
    with (root/'data/q1_targets.tsv').open() as f:
        targets = list(csv.DictReader(f, delimiter='\t'))
    if len(targets) != 2 or any(set(t) != {'label','contig','position','ref','alt'} for t in targets):
        raise SystemExit('Unexpected target schema')
    private, safe = {}, {}
    for stage, bam in bams.items():
        if not bam.is_file():
            raise SystemExit('Required BAM missing: ' + stage)
        check = subprocess.run(['samtools','quickcheck',str(bam)],capture_output=True)
        if check.returncode:
            raise SystemExit('BAM quickcheck failed: ' + stage)
        private[stage], safe[stage] = [], []
        for i, target in enumerate(targets):
            pos = int(target['position'])
            region = '{}:{}-{}'.format(target['contig'], max(1,pos-100),pos+100)
            result = subprocess.run(['samtools','view',str(bam),region],capture_output=True,text=True)
            if result.returncode:
                raise SystemExit('BAM query failed: ' + stage)
            detail, summary = analyze(result.stdout.splitlines(), target)
            private[stage].append(detail)
            safe[stage].append(dict(candidate='candidate_{}'.format(i+1), **summary))
    report = {'analysis':'posthoc_ref_alt_orientation_single_observation_groups',
        'limitations':[
            'After-duplicate-filtering BAMs only; MAPQ/BQ >=20; QC-failed alignments excluded.',
            'Group identity is RG plus query name within a lane.',
            'Multiple qualified observations per group are excluded from orientation tables; this changes the analyzed subset.',
            'Tests use observed read alignment strand, not inferred template orientation.',
            'Nominal Fisher tests are exploratory and not multiplicity-adjusted.',
            'No detected association does not establish absence of strand bias.',
            'No cross-lane pooling, library assumption, genotype decision or threshold change.'
        ],'stages':safe}
    os.umask(0o077)
    out=Path(tempfile.mkdtemp(prefix='q1_strand_review_',dir=str(root/'out')))
    (out/'private').mkdir(); (out/'return').mkdir()
    (out/'private/details.json').write_text(json.dumps(private,indent=2)+'\n')
    (out/'private/script_sha256.txt').write_text(hashlib.sha256(Path(__file__).read_bytes()).hexdigest()+'\n')
    (out/'return/q1_strand_safe.json').write_text(json.dumps(report,indent=2)+'\n')
    print('STRAND_REVIEW_COMPLETE')
    print('PRIVATE_RUN_DIR='+str(out))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
