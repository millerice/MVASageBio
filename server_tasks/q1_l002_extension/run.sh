#!/usr/bin/env bash
# Linux; usage: bash run.sh /home/mva_q2
set -euo pipefail
umask 077
ROOT=${1:-/home/mva_q2}
TASK=$(cd "$(dirname "$0")" && pwd)
for tool in samtools minimap2 python3 sha256sum flock tar; do
  command -v "$tool" >/dev/null || { echo "Missing tool: $tool"; exit 1; }
done
[[ -d "$ROOT/out" && -d "$ROOT/data" ]] || { echo 'Invalid server root'; exit 1; }
exec 9>"$ROOT/out/q1_l002_extension.lock"
flock -n 9 || { echo 'Another L002 task is running'; exit 1; }
RUN=$(mktemp -d "$ROOT/out/q1_l002_$(date -u +%Y%m%dT%H%M%SZ)_XXXXXX")
mkdir "$RUN/logs" "$RUN/private" "$RUN/return" "$RUN/tmp"
echo "RUN_DIR=$RUN"
trap 'code=$?; if [ "$code" -ne 0 ]; then echo "FAILED exit=$code run=$RUN"; fi' EXIT
REF=$ROOT/ref/GRCh38.primary.fa
TARGETS=$ROOT/data/q1_targets.tsv
VALIDATOR=$ROOT/q1_full_reference_recheck/validate_bam.py
BEFORE=$ROOT/out/wg_l001.bam
AFTER=$ROOT/out/q1_full_reference/full.dedup.bam
PREFIX=$ROOT/data/WGS_EX2312012_HGWCNDSX7_S16_L002
R1=${PREFIX}_R1_001.fastq.gz
R2=${PREFIX}_R2_001.fastq.gz
for file in "$REF" "$REF.fai" "$TARGETS" "$VALIDATOR" "$BEFORE" "$AFTER" "$R1" "$R2"; do
  [[ -s "$file" ]] || { echo 'Required input missing or empty'; exit 1; }
done
MINIMAP_VERSION=$(minimap2 --version)
SAMTOOLS_VERSION=$(samtools --version | sed -n '1p')
[[ "$MINIMAP_VERSION" == '2.31-r1302' && "$SAMTOOLS_VERSION" == 'samtools 1.9' ]] || { echo 'Tool versions differ from planned server versions'; exit 1; }
python3 - "$ROOT" "$RUN" <<'PY'
import shutil, sys
from pathlib import Path
root, run = map(Path, sys.argv[1:])
if shutil.disk_usage(run).free < 180 * 1024**3:
    raise SystemExit('Require at least 180 GiB free for retained intermediates')
memory = dict((s.split(':', 1)[0], int(s.split()[1])) for s in Path('/proc/meminfo').read_text().splitlines())
if memory.get('MemAvailable', 0) < 20 * 1024**2:
    raise SystemExit('Require at least 20 GiB currently available memory')
PY
check_hash() {
  local file=$1 expected=$2 actual
  actual=$(sha256sum "$file"); actual=${actual%% *}
  [[ "$actual" == "$expected" ]] || { echo 'Input or validator SHA256 mismatch'; exit 1; }
  printf '%s  %s\n' "$actual" "$(basename "$file")" >> "$RUN/private/input_checksums.sha256"
}
echo 'STAGE 1: frozen validator, reference, targets and L002 input checksums'
check_hash "$VALIDATOR" 58fe849bda2cafed0b0de9a658ed8251142e29e793b01ea40634f34a117567da
check_hash "$REF" 1e74081a49ceb9739cc14c812fbb8b3db978eb80ba8e5350beb80d8ad8dfef3b
check_hash "$TARGETS" d1446b44b77ec29577fb149b06b86c302d63653e5a264bcddb9fc5ef61e909d4
check_hash "$R1" 0f60e090d9873a18a6914d374fa070a20502aa546d05b51ec520bd9e06ae7e71
check_hash "$R2" 992ee50db8a89709b7adb327daabcacbf58261503f8c439bb18a3c682e43cd91
samtools quickcheck "$BEFORE" "$AFTER"
python3 -B "$TASK/summarize.py" --validator "$VALIDATOR" --targets "$TARGETS" --reference "$REF" --check-only
{
  printf 'minimap2 %s\n' "$MINIMAP_VERSION"
  printf '%s\n' "$SAMTOOLS_VERSION"
  python3 --version
  echo 'alignment_threads=12 sort_extra_threads=2 sort_memory_per_thread=1G'
  echo 'L002 RG=Q1_L002 SM=PROBAND01 LB=omitted_unknown'
  echo 'No L001+L002 merge; library relationship unverified'
  echo 'secondary=no; mapped reads retained, matching prior Q2 source BAM policy'
} > "$RUN/return/versions_and_method.txt"
sha256sum "$TASK/run.sh" "$TASK/summarize.py" "$VALIDATOR" > "$RUN/private/code_checksums.sha256"
echo 'STAGE 2: L002 complete-reference alignment and name sort'
minimap2 -ax sr --secondary=no -t 12 -R '@RG\tID:Q1_L002\tSM:PROBAND01\tPL:ILLUMINA\tPU:L002' "$REF" "$R1" "$R2" 2> "$RUN/logs/minimap2.log" \
  | samtools view -u -F 4 - \
  | samtools sort -n -@ 2 -m 1G -T "$RUN/tmp/name" -o "$RUN/l002.namesort.bam" -
echo 'STAGE 3: fixmate and coordinate sort'
samtools fixmate -m -@ 2 "$RUN/l002.namesort.bam" "$RUN/l002.fixmate.bam"
samtools sort -@ 2 -m 1G -T "$RUN/tmp/coord" -o "$RUN/l002.before.bam" "$RUN/l002.fixmate.bam"
samtools index "$RUN/l002.before.bam"
echo 'STAGE 4: mark duplicates (retain marks), then materialize excluded-duplicate BAM'
samtools markdup -@ 2 -s "$RUN/l002.before.bam" "$RUN/l002.marked.bam" 2> "$RUN/logs/markdup_stats.txt"
samtools index "$RUN/l002.marked.bam"
samtools view -@ 2 -b -F 1024 -o "$RUN/l002.after.bam" "$RUN/l002.marked.bam"
samtools index "$RUN/l002.after.bam"
samtools quickcheck "$RUN/l002.before.bam" "$RUN/l002.marked.bam" "$RUN/l002.after.bam"
echo 'STAGE 5: same-validator comparison across both lanes'
python3 -B "$TASK/summarize.py" --validator "$VALIDATOR" --targets "$TARGETS" --reference "$REF" \
  --l001-before "$BEFORE" --l001-after "$AFTER" \
  --l002-before "$RUN/l002.before.bam" --l002-after "$RUN/l002.after.bam" --output "$RUN"
cd "$RUN/return"
sha256sum q1_l002_safe_summary.json versions_and_method.txt > RETURN_CHECKSUMS.sha256
tar -czf "$RUN/q1_l002_return_bundle.tar.gz" q1_l002_safe_summary.json versions_and_method.txt RETURN_CHECKSUMS.sha256
echo "Q1_L002_COMPLETE bundle=$RUN/q1_l002_return_bundle.tar.gz"
