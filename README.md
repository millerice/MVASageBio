# MVASageBio — JiuTian Bio · MVA Hackathon 2026 (Track 2 submission)

Repository accompanying the **Track 2 (drug repurposing) submission of team JiuTian Bio** to the
[Sage Bionetworks "Rare Disease, Real Kid: MVA Hackathon 2026"](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026).
Single registered participant; report-author-facing disclosure in the report §0.

## Submission package

| Component | Where |
|---|---|
| Report (the submitted file) | [`reports/JiuTian-Bio_track2_report.md`](reports/JiuTian-Bio_track2_report.md) |
| Pitch video (2:59, unlisted YouTube) | https://youtu.be/sKnrdGWi8o8 |
| This repository | kept public through the review window |

Track 2 submission logged 2026-10-03 (1 of 3 allowed; only the latest submission is reviewed).

## What this is (short version — the report is authoritative)

- **Track 1**: our *BUB1B* compound-heterozygous answer received an **official Track 1 full match**
  [EV-0042]; that confirmed genotype anchors the Track 2 mechanism section (report §1).
- **Track 2**: a source-graded, ledger-traced mechanism chain (14 nodes; every claim tagged
  fact/inference/hypothesis with tier 0–4 sources) → component screen + product-level FDA label
  verification of **market-approved drugs only** → penalty-aware research-priority scoring with
  five-scenario rank sensitivity → two nominated research hypotheses on independent axes
  (**everolimus**, mTORC1-sarcopenia axis; **metformin**, energy-stress axis), with chloroquine held
  out as a high-risk mechanistic probe and niacinamide excluded at the market-approval gate
  (rationale retained, §2.1). Every drug statement is a **falsifiable research hypothesis with
  stated counter-evidence — nothing in this repository is a treatment recommendation**.

## Repository map

| Path | Contents |
|---|---|
| `research/evidence.jsonl` | Public evidence ledger (94 entries, EV-0001…); every substantive report claim cites an EV number |
| `research/mechanism_chain.json` | Machine-readable mechanism chain (14 nodes / 15 edges, per-node grading) |
| `research/report_claims.tsv`, `research/review_attestations.jsonl` | Claim registry; hash-bound review attestations (current row binds the submitted report's sha256) |
| `research/*.tsv` | Seed pool, product status, tracked scoring inputs |
| `src/track2_repurposing/` | `ledger.py` (schema lint) · `validate_chain.py` (chain×ledger×claims cross-audit) · `build_drug_pool.py` (openFDA screening) · `score_candidates.py` (scoring + sensitivity) · tests |
| `src/track1_variant/` | Track 1 local scoring harness built on the official evaluation core |
| `src/common/` | `validate_all.py` top-level gate |
| `reports/` | Submitted reports (Track 1, Track 2) + filled Track 1 methods form |
| `submissions/` | Submission records: receipts, quota use, pre-public repo scan |
| `docs/` | Internal working documents (Chinese): architecture, rules analysis, milestone gates, status checkpoints, `llm-usage.log` |
| `data/` | Intentionally empty in git — see privacy note |
| `references/` | Official pages/templates snapshot (incl. methods form template, evaluation source) |

Ledger schema: [`research/README.md`](research/README.md).

## Genomic-data privacy

Per the dataset's genomic-data rules, **no genomic data (VCF/BAM/FASTQ) and no variant-level
detail (coordinates, alleles, HGVS, read counts) enters this repository**. `data/` paths are
gitignored, and a pre-publication scan of the *entire git history* (including unreachable objects)
verified zero genomic content — see `submissions/track2/2026-10-03_repo-public-prescan.md`.
Public artifacts stay at gene/domain granularity; a small controlled private appendix (never
published) holds variant-level evidence entries whose IDs may be cited publicly without content.

## Reproducibility

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/track2_repurposing/ledger.py lint
.venv/bin/python src/track2_repurposing/validate_chain.py
.venv/bin/python src/track2_repurposing/score_candidates.py --check-only
.venv/bin/python src/common/validate_all.py   # top-level gate
```

Scope honesty: scoring and validation code is public here; the historical alignment/QC ran on a
private compute node whose scripts and BAMs remain private under the data rules — the full
partial-reproducibility statement is report §5.

## Generative-AI use

Disclosed in **report §0**; the complete interaction log is `docs/llm-usage.log`. Uses include
drafting/review assistants selected for Processor-type API terms, independent cross-review
sessions, and MiniMax text-to-speech for the pitch video's narration (human-written public-tier
script; the terms deviation is assessed and logged).

## License & acknowledgments

Released under **CC-BY 4.0** per hackathon rules.

> *This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with
> the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for
> Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their
> family who generously contributed their data and their story to advance research into this rare
> disease. We acknowledge their trust in making this Hackathon possible.* [EV-0082]

Dataset citation: *Rare Disease, Real Kid: MVA Hackathon 2026 - Dataset.* Synapse syn76251147
(https://www.synapse.org/Synapse:syn76251147); controlled-access data via Hugging Face
(SageBio/mva-hackathon-2026-data) [EV-0096].

## Links

- Hackathon Space (submissions, rules, discussions): https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026
- Dataset (gated): https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data
- Synapse project: https://www.synapse.org/Synapse:syn76251147
- Track 1 scoring reference (Stenton 2024, CAGI6-RGP): https://doi.org/10.1186/s40246-024-00604-w
- Submissions close 2026-10-24 23:59 UTC
