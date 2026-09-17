# Track 1 Methods Report — v0

**Team**: JiuTian Bio · **Date**: 2026-09-08 · **Track**: T1 Variant Prediction · **Model**: 1 of 1

> Per the hackathon data-use terms, this public methods report contains no variant-level genotype data of the proband; candidate variants were submitted only through the official CSV channel. Gene-level conclusions and interpretation logic are published under CC-BY.

## 1. Approach (form Q: "describe your model/approach in detail")

A phenotype-driven, evidence-tiered pipeline for compound-heterozygous (comp-het) discovery in a singleton, unphased WGS VCF:

1. **QC & normalization** — full-callset statistics (5,012,204 variants; 4,740,790 PASS; SNV/indel and zygosity profile); audited contig style (no `chr` prefix in the source VCF) with prefix conversion enforced at submission packaging.
2. **Gene prioritization** — the three established mosaic variegated aneuploidy (MVA) genes ranked by disease-type concordance with the proband's HPO profile (rhabdomyosarcoma, failure to thrive / short stature, prematurity, small for gestational age, parental recurrent pregnancy loss): **BUB1B (MVA1), CEP57 (MVA2), TRIP13 (MVA3)**.
3. **Per-gene region annotation** — for each gene region (±5 kb), all proband PASS variants were annotated against region-sliced **gnomAD v4.1** sites data (AF, AC/AN, nhomalt, faf95, CADD PHRED, REVEL, SpliceAI, VEP consequences) and **ClinVar** (significance, review status). Private alleles absent from gnomAD were annotated via **Ensembl VEP REST** against the MANE transcript (SIFT/PolyPhen, HGVS).
4. **Comp-het calling** — within a candidate gene, require two heterozygous variants that are individually rare (AF < 0.01; loss-of-function candidates held to stricter population evidence including zero observed homozygotes), functionally consequential (VEP HIGH/MODERATE, with NMD-sensitivity for truncating variants), and phenotype-consistent. One stop-gain plus one private, dual-algorithm-deleterious missense in **BUB1B** satisfy all criteria; both map to the kinase domain.
5. **Differential exclusion** — CEP57 and TRIP13 regions were processed through the identical pipeline and contained no coding-variant hits; both were excluded.
6. **Packaging preflight** — a local scoring harness importing the official `evaluation.py` kernel verified the 12-column template, `PROBAND01`, epcr range, finding_type, `chr` prefix on every filled chromosome field, and complete `chrom_2/pos_2/ref_2/alt_2` whenever a second allele is started. Rank points were checked only against a mock-truth simulation (format path), not against a hidden official key.

## 2. Automation level (form Q11–Q12)

Hybrid. Filtering, annotation, and frequency/consequence triage were fully automated (bcftools/htslib pipeline). Final candidate selection and row construction were manually curated: review of ClinVar star level and disease-name concordance, gnomAD AF/nhomalt/faf95, consequence and NMD reasoning, differential-gene exclusion, and local scorer preflight.

## 3. Data sources (form Q13–Q15)

**Public data only** (in addition to the organizer-provided proband VCF):

| Source | Version/snapshot | Use |
|---|---|---|
| gnomAD sites, genomes | v4.1 (region slices) | AF/AC/AN, nhomalt, faf95, CADD, REVEL, SpliceAI, VEP consequences |
| ClinVar VCF (GRCh38) | NCBI snapshot 2026-09 | Pathogenicity, review status, disease nomenclature |
| Ensembl VEP REST | current | Consequence, SIFT/PolyPhen, HGVS for private alleles |
| OMIM | via prior literature review | MVA gene–subtype assignment (BUB1B=MVA1, CEP57=MVA2, TRIP13=MVA3) |
| Official Space source (rules, scoring kernel) | snapshot 2026-09-08 | Submission format, scoring verification |

**Proprietary data**: none.

## 4. Comp-het output capability (form Q16)

Yes — the approach outputs comp-het pairs natively: both variants are emitted on a single row (`chrom_1..alt_2` complete), consistent with the submission format.

## 5. Secondary / incidental findings (form Q17)

v0 contains a single `primary` row; no secondary or incidental findings met inclusion criteria.

## 6. Runtime & cost (form Q18)

≈ 4 hours wall clock on a single laptop (macOS; bcftools/htslib 1.24). Downloads ≈ 220 MB (ClinVar release + per-gene gnomAD region slices). Compute cost negligible; one analyst with LLM assistance.

## 7. Limitations

- The VCF is unphased with no parental samples: the trans configuration of the comp-het pair is a Bayesian inference (two ultra-rare damaging hits in a recessive disease gene), not directly demonstrated; read-backed phasing was deferred (no BAM in dataset).
- CNV/SV analysis not performed (callset is SNV/indel-only).
- Genome-wide unbiased comp-het scanning was deferred in v0 (candidate-gene scan only) — the differential set covers all established MVA genes.
- EPCR is a subjective posterior estimate.

## 8. Generative-AI disclosure (form Q10, required)

> **Initial workflow: Anthropic Claude via Claude Code. Subsequent review and revisions: OpenAI Codex desktop.**

The initial September 8 workflow used Claude Code for pipeline design, coding, analysis assistance,
and documentation. The usage log records a commercial Anthropic API plan and processing of
variant-level candidate coordinates, genotypes, and annotations, without raw VCF/FASTQ transfer
or model-output scoring feedback in that workflow. Subsequent September 15–17 Codex desktop
sessions reviewed code and private historical materials, interpreted returned diagnostic summaries,
and assisted with revisions. These later sessions must not be described as using public material only.
Scientific claims must trace to the evidence ledger; automated checks do not establish completed
human verification of every claim. The full interaction inventory, account-specific service terms,
and final independent review remain pending, as recorded in `docs/llm-usage.log`.
This disclosure addendum does not imply that the later diagnostics formed part of the September 8 submission.

## 9. License

This report is released under CC-BY 4.0 as required by the hackathon rules.
