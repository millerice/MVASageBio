#!/usr/bin/env bash
# Q1 complete-reference reconciliation, aligned to the existing Q2 server layout.
# Usage: bash q1_full_reference_recheck/run_q1_full_reference.sh [threads] [server_root]
set -euo pipefail
THREADS=${1:-16}
TASK_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT=${2:-$(cd "$TASK_DIR/.." && pwd)}
REF_DIR=$ROOT/ref; DATA_DIR=$ROOT/data; OUT=$ROOT/out; Q1_OUT=$OUT/q1_full_reference
LOG=$Q1_OUT/logs; PRIVATE=$Q1_OUT/private; EXPORT=$Q1_OUT/return
REF=$REF_DIR/GRCh38.primary.fa
R1=$DATA_DIR/WGS_EX2312012_HGWCNDSX7_S16_L001_R1_001.fastq.gz
R2=$DATA_DIR/WGS_EX2312012_HGWCNDSX7_S16_L001_R2_001.fastq.gz
TARGETS=$DATA_DIR/q1_targets.tsv  # private server-only input; never return or commit

mkdir -p "$LOG" "$PRIVATE" "$EXPORT"
exec > >(tee -a "$LOG/run_q1.log") 2>&1
umask 077
echo "=== $(date -u +%FT%TZ) Q1 full-reference reconciliation; root=$ROOT; threads=$THREADS ==="
for tool in samtools minimap2 python3 sha256sum; do command -v "$tool" >/dev/null || { echo "Missing tool: $tool"; exit 1; }; done
for file in "$REF" "$R1" "$R2" "$TARGETS"; do [[ -r "$file" ]] || { echo "Unreadable required input: $file"; exit 1; }; done
verify_sha() {
  local file=$1 expected=$2 actual
  actual=$(sha256sum "$file" | cut -d' ' -f1)
  [[ "$actual" == "$expected" ]] || { echo "Input checksum mismatch: $(basename "$file")"; exit 1; }
  echo "input checksum PASS: $(basename "$file")"
}
# Same controlled L001 inputs and checksums used by the existing Q2 task.
verify_sha "$R1" 5ec244c0648552f2b23ae5b1a0b1350e8e464eb5cccd40178a109c44c174939f
verify_sha "$R2" b80f2cc9f29c229a2bfe557988a4b93c74494fc0d9108b3752bc04cf57239cab
samtools faidx "$REF"

# Verify target bases without emitting private locus/allele information.
python3 - "$REF" "$TARGETS" <<'PY'
import csv, subprocess, sys
ref, targets = sys.argv[1:]
with open(targets) as handle: rows = list(csv.DictReader(handle, delimiter='\t'))
if len(rows) != 2 or set(rows[0]) != {'label','contig','position','ref','alt'}:
    raise SystemExit('private q1_targets.tsv has invalid schema')
for row in rows:
    locus = f"{row['contig']}:{row['position']}-{row['position']}"
    body = subprocess.check_output(['samtools','faidx',ref,locus], text=True).splitlines()
    base = ''.join(x for x in body if not x.startswith('>')).upper()
    if base != row['ref'].upper(): raise SystemExit(f"reference-base mismatch for target label {row['label']}")
print('private target/reference consistency PASS')
PY
{
  printf 'minimap2 '; minimap2 --version
  samtools --version | head -n1
  python3 --version
  printf 'reference_sha256 '; sha256sum "$REF" | cut -d' ' -f1
  printf 'r1_sha256 '; sha256sum "$R1" | cut -d' ' -f1
  printf 'r2_sha256 '; sha256sum "$R2" | cut -d' ' -f1
} > "$EXPORT/versions.txt"

# Reuse Q2's full-reference BAM if retained; otherwise remap the same validated L001 input.
SOURCE_BAM=$OUT/wg_l001.bam
if [[ -r "$SOURCE_BAM" ]]; then
  echo "Reusing retained Q2 full-reference BAM"
  samtools quickcheck -v "$SOURCE_BAM"
  samtools sort -n -@ "$THREADS" -o "$Q1_OUT/full.namesort.bam" "$SOURCE_BAM"
else
  echo "Q2 BAM absent: rebuilding full-reference alignment from L001 FASTQ"
  minimap2 -ax sr -t "$THREADS" --secondary=no "$REF" "$R1" "$R2" 2> "$LOG/minimap2_q1.log" | samtools sort -n -@ "$THREADS" -o "$Q1_OUT/full.namesort.bam" -
fi
samtools fixmate -m -@ "$THREADS" "$Q1_OUT/full.namesort.bam" "$Q1_OUT/full.fixmate.bam"
samtools sort -@ "$THREADS" -o "$Q1_OUT/full.sorted.bam" "$Q1_OUT/full.fixmate.bam"
samtools markdup -@ "$THREADS" -r "$Q1_OUT/full.sorted.bam" "$Q1_OUT/full.dedup.bam"
samtools index -@ "$THREADS" "$Q1_OUT/full.dedup.bam"
samtools flagstat "$Q1_OUT/full.dedup.bam" > "$LOG/flagstat_dedup.txt"
python3 "$TASK_DIR/validate_bam.py" --bam "$Q1_OUT/full.dedup.bam" --targets "$TARGETS" --private-detail "$PRIVATE/q1_private_detail.tsv" --safe-summary "$EXPORT/q1_safe_summary.json"
cd "$EXPORT"
sha256sum q1_safe_summary.json versions.txt > RETURN_CHECKSUMS.sha256
tar -czf "$ROOT/q1_return_bundle.tar.gz" q1_safe_summary.json versions.txt RETURN_CHECKSUMS.sha256
echo "=== completed. Return only: $ROOT/q1_return_bundle.tar.gz ==="
echo "Controlled outputs remain in $Q1_OUT; retain/delete only under the data-retention policy."
