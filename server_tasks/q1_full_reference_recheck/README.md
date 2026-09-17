# Q1 full-reference read-support recheck (server task package)

This package is deliberately safe to commit: it contains no FASTQ, VCF, target
coordinates, alleles, credentials, or results. Copy it into the **existing Q2 server
root**: it intentionally reuses Q2's `ref/`, `data/`, and `out/` layout. Run it only
in the controlled-data environment. Do **not** copy BAM/CRAM, VCF, pileup, or
private-detail outputs back to this repository.

## Purpose and decision boundary

This is a reconciliation of the earlier mini-reference raw-read-support check, not an
independent clinical validation. It maps the supplied FASTQ pairs to a complete GRCh38
reference, applies coordinate-based duplicate removal, and checks two private candidate SNVs with
MAPQ >=20 and base quality >=20. It also tests whether one short-read molecule covers
both loci.

The frozen validator emits `not_establishable_short_read_geometry` when it finds no
shared qualified query name. That observation establishes neither trans phase nor the
impossibility of every short-read phasing approach. Chained phasing has not been assessed.
The L002 summary uses the narrower status `not_established_no_shared_qualified_query_name`.

## Server prerequisites

- Linux with `bash`, `python3`, `sha256sum`, `samtools`, and `minimap2`.
- The Q2 server root, with `ref/GRCh38.primary.fa` and the validated L001 pair already
  present under `data/`.
- A private `data/q1_targets.tsv` with the schema below.
- A **private**, server-only target TSV. Never commit or transmit it in chat.

Create the private target file with this schema (header mandatory):

```text
label\tcontig\tposition\tref\talt
candidate_1\t<private>\t<private>\t<private>\t<private>
candidate_2\t<private>\t<private>\t<private>\t<private>
```

Only biallelic SNVs are supported by the bundled CIGAR parser. If either target is an
indel, stop and ask for an indel-aware version rather than treating its count as zero.

## Example

Copy `q1_full_reference_recheck/` to the Q2 server root, then run:

```bash
bash q1_full_reference_recheck/run_q1_full_reference.sh 24
```

If `out/wg_l001.bam` from Q2 remains on the server, the task reuses that complete
reference alignment; otherwise it remaps the same validated L001 input. In both cases
it repeats name sorting, `fixmate`, duplicate removal, and Q1 validation. It writes:

- `out/q1_full_reference/private/q1_private_detail.tsv`: counts and target-associated
  detail. Keep on the controlled server.
- `out/q1_full_reference/return/q1_safe_summary.json`: only candidate labels, pass/fail states, direct-phase
  status, tool versions, and checksums. This is the only analysis result suitable to
  return here, together with `versions.txt` and `RETURN_CHECKSUMS.sha256`, packaged as
  `q1_return_bundle.tar.gz` at the Q2 server root.

Before returning files, inspect them manually and ensure no paths, coordinates, alleles,
read names, depth counts, or BAM/VCF content are included.

## Interpretation

`read_support_pass` requires at least five non-duplicate ALT observations after the
quality filters, an ALT fraction in [0.30, 0.70], and no contradictory mate observation
for that target. The support-count and allele-balance thresholds belong to the original
plan; the zero-mate-conflict veto was added later. The frozen validator's comment calling
that veto pre-registered is inaccurate. These are consistency criteria, not a clinical
genotype call; L002 reporting separates the original thresholds from the added veto.

The full-reference output can strengthen the limited statement “raw-read support was
rechecked against a complete reference.” It cannot establish trans without a molecule
linking both loci, parental data, long reads, or another suitable phasing assay.

## Frozen implementation and known limits (2026-09-17)

`validate_bam.py` is hash-pinned by the L002 task. Its bytes and the archived task
packages are retained for historical reproducibility; these clarifications do not alter
past results. It does not exclude QC-failed records itself and does not veto a large
OTHER-base component. Separate returned diagnostics reported no qualified OTHER bases,
mate conflicts, or qualified ALT QC-fail flags in the examined stages; those fields do
not establish the QC-fail status of every REF observation [EV-0089]. The BAM reuse branch
performs quickcheck but does not itself bind that BAM to the validated FASTQ/reference.
Historical execution provenance remains under review. Duplicate filtering and query-name
grouping do not prove full molecular independence.

## Operational safety

- Use a least-privilege account and SSH key authentication; do not share passwords in
  chat or place credentials in this directory.
- Keep the private target file, BAM, pileup, VCF, and detailed result outside Git.
- On completion, retain or delete controlled intermediates according to the hackathon
  data-retention rules; the package makes no deletion decision automatically.
