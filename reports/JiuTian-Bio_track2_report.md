# Track 2 Proposal — Repurposing Market-Approved Drugs for Mosaic Variegated Aneuploidy Syndrome Type 1 (BUB1B)

**Team**: JiuTian Bio · **Submitter**: millerkai · **Date**: 2026-09 (v1) · **Track**: 2 — Drug Repurposing

> Evidence discipline: every substantive claim in this report cites an entry number (EV-xxxx) from our
> evidence ledger (85 entries; `research/evidence.jsonl` in the accompanying repository). Tier-0 sources are
> official pages/rules/labels/source code; tier-1 are peer-reviewed literature. Conflicts between sources are
> flagged inline, not smoothed over. All drug statements are **research hypotheses with testable predictions
> and stated counter-evidence** — nothing in this document is a treatment recommendation.

---

## 0. Generative-AI disclosure (form A9, required)

> **Anthropic API, Claude (Claude Code), commercial terms, no training on customer content.**

Generative AI (Claude, via the Claude Code CLI on a commercial API plan that does not train on customer
content) was used as an interactive assistant throughout: (i) exploratory variant triage of the controlled
VCF against public frequency/annotation resources (Track 1); (ii) literature search triage and abstract
extraction against PubMed/NCBI E-utilities; (iii) drafting and code assistance for the analysis pipeline,
evidence ledger, and this report. All scientific claims were verified by the human author against the cited
sources before entry into the evidence ledger, and the ledger — not the model — is the only permitted source
for report claims (reporter isolation). Model outputs were not submitted for vendor scoring or feedback.
Data interactions with LLM services are logged in `docs/llm-usage.log`.

## Abstract (form A17; strengths and limitations included)

Mosaic variegated aneuploidy (MVA) syndrome type 1 is caused by biallelic loss-of-function of **BUB1B**,
encoding the spindle assembly checkpoint (SAC) kinase BUBR1. In the proband of this hackathon dataset we
characterized a compound-heterozygous genotype: a nonsense allele in an NMD-sensitive exon (a functional
null) paired with a kinase-domain missense allele that the literature class explains primarily as a
**protein-destabilizing hypomorph** — MVA1 kinase-domain missense mutants reduce BUBR1 protein abundance
5–10× via proteasomal clearance, while kinase catalysis itself is dispensable for checkpoint signaling.
The resulting BUBR1 insufficiency weakens SAC control (quantitatively: ~13% expression preserves
segregation fidelity, ~6% does not), producing mosaic variegated aneuploidy and the proband's phenotype
(rhabdomyosarcoma, growth failure, sarcopenia, parental recurrent pregnancy loss). We assembled this
mechanism as a machine-readable, ledger-traced chain (14 nodes, every claim source-graded), and asked a
repurposing question the field has not yet answered: with **zero** registered interventional trials for
MVA/BUB1B (ClinicalTrials.gov, tier-0 query), which *market-approved* drugs act on nodes of this chain?
Because BUBR1 loss is not classically druggable, we targeted two non-obvious properties: (i) the pathogenic
mechanism is **abundance**, not catalysis — and BUBR1 abundance is pharmacologically raisable via the
SIRT2–NAD+ axis; (ii) downstream stress axes (mTORC1-driven sarcopenia, aneuploid-cell metabolic stress,
selective aneuploid-cell clearance) are druggable with approved compounds. From a seed pool of nine
mechanism-matched compounds, automated openFDA verification (tier-0) confirmed marketing status for six;
transparent scoring selected four candidates on independent axes: **niacinamide** (NAD+ precursor;
RCT-level human precedent for cancer-chemopreventive efficacy), **metformin** (energy-stress modulation
with cross-species protection in aneuploidy models), **chloroquine** (selective anti-proliferative effect
on aneuploid cells validated in a BubR1-insufficient MVA mouse model), and **everolimus** (mTORC1 axis;
the deepest pediatric experience with chronic mTOR inhibition, from TSC-SEGA trials). For each candidate
we state a falsifiable prediction — primarily in the *C. elegans* SAC-weakening platform that the MVA
Society itself funds (san-1/MAD3 is the worm BUBR1-family homolog), plus patient-cell biomarker readouts
— and the specific counter-evidence that could refute the hypothesis (evidence-transfer gaps, pediatric
safety burdens, and one acknowledged direction-of-effect tension between "clear aneuploid cells" and
"support aneuploid-cell fitness", which we separate by clinical scenario). **Strengths**: full claim
traceability (ledger + automated validators), source-grading, conflict disclosure, and market-approval
verification by official API rather than assertion. **Limitations**: the compound-heterozygous *trans*
configuration is inferred (short-read data cannot phase two variants >10 kb apart; no parental samples);
the destabilization mechanism is inferred from the allele class rather than assayed in patient cells;
dose thresholds derive from cell/mouse systems; and no candidate has been tested in MVA. This framework —
controlled genotype → ledger-enforced mechanism chain → mechanism-matched approved-drug ranking →
falsifiable predictions — is reusable for any rare-disease N-of-1 analysis. *(438 words)*

---

## 1. Variant mechanism characterization (form A15; submission-page hard requirement)

### 1.1 Genotype (report-level granularity)

The proband carries a compound-heterozygous **BUB1B** genotype (trans configuration inferred; see §6),
confirmed as the Track 1 official answer (full match [EV-0042]):

| Allele | HGVS (NM_001211.5) | Protein | Class |
|---|---|---|---|
| 1 | c.2210T>G | p.Leu737Ter | Nonsense, exon 17/23 (NMD-sensitive) → **functional null** [EV-0039, EV-0048] |
| 2 | c.3006T>G | p.Asn1002Lys | Missense, kinase-domain C-terminal edge (10 aa from the known MVA1 allele L1012P in the αG-helix region) → **destabilizing hypomorph** (inference; [EV-0040, EV-0044, EV-0045]) |

Supporting observations: allele 1 is ClinVar P/LP for MVA1, gnomAD AF ≈ 3×10⁻⁵ with zero homozygotes,
CADD 38 [EV-0039]; allele 2 is absent from gnomAD (all populations), SIFT 0.01 / PolyPhen 0.997 [EV-0040].
Both loci show balanced heterozygous read support in the proband VCF (no locus-level LOH/mosaicism)
[EV-0077-private]. Both alleles were additionally re-validated at read level from the raw sequencing
data (one lane, ~12×, aligned to a coordinate-true BUB1B mini-reference; MAPQ≥20, BQ≥20,
fragment-deduplicated): each allele is supported by ≥5 independent ALT fragments with balanced allele
fractions [EV-0084]. This genotype architecture (truncating null + kinase-domain missense) matches the
published rule for surviving MVA1 — two complete nulls have never been reported [EV-0047].

### 1.2 Mechanistic chain (LoF character; pathway disrupted; downstream consequences)

```
N1  BUB1B comp-het (null + destabilized hypomorph)
 ├── N2  nonsense allele → NMD → functional null [EV-0039, EV-0048]   (patient-derived evidence)
 ├── N3  missense allele → protein destabilization (5–10× lower abundance,                 (inference from
 │        proteasomal clearance, HSP90-dependent folding; kinase activity dispensable)      allele class)
 │        [EV-0040, EV-0044, EV-0045]
 ↓  (architecture rule: truncating + kinase missense [EV-0047])
 N5  BUBR1 protein INSUFFICIENCY (dose-dependent)
 │     ~13% expression → segregation fidelity preserved; ~6% → mis-segregation in most cells [EV-0046]
 │     mouse dose series: progeroid/dwarfism/cancer at low dose, massive apoptosis at very low dose [EV-0050]
 ↓
 N6  SAC weakening: insufficient MCC–APC/C inhibition → shortened mitosis, PSCS [EV-0044, EV-0049, EV-0055]
 ↓
 N7  MOSAIC VARIEGATED ANEUPLOIDY (~25–50% of patient cells random gains/losses) [EV-0049, EV-0055]
 ↓ ↓ ↓ ↓  (four phenotype branches)
 ├─ N8  growth failure: progenitor apoptosis → tissue hypoplasia (93.5% of MVA patients) [EV-0050, 0051, 0055]
 ├─ N9  parental RPL: BubR1-null embryos die E7.5–E13.5; SAC insufficiency predicted to drive a
 │       significant fraction of human RPL (authors' inference) [EV-0049, EV-0056]
 ├─ N10 cancer predisposition: Wilms > rhabdomyosarcoma (proband's index tumor) > ALL;
 │       malignancy 38.7% (case series) vs ~75% (Orphanet) — SOURCES CONFLICT, report the range [EV-0051 conflict, EV-0052]
 └─ N11 progeroid–sarcopenia: mTORC1 hyperactivity + p19Arf-senescence axis (mouse) [EV-0057]
 (+) N13 systemic stress: chronic immune response component beyond tumor susceptibility [EV-0061]
```

**HPO alignment of the proband's 8 phenotype terms**: 6/8 map strongly onto the chain (rhabdomyosarcoma→N10,
short stature / failure to thrive / SGA→N8, muscle atrophy→N11, parental RPL→N9); prematurity aligns
indirectly (no published MVA–prematurity analysis; plausible via placental insufficiency, stated as such);
**nephrocalcinosis has no published MVA/BUB1B association** and is reported honestly as an unexplained
observation, not a mechanism claim [EV-0054]. The ciliopathy hypothesis for MVA remains directly
contradicted in the literature [EV-0053 conflict] and is not used.

### 1.3 Why BUB1B loss is "undruggable" — and what is actually druggable

BUBR1 loss of function looks like a classical undruggable problem: one cannot agonize a missing
tumor-suppressor-like checkpoint protein. Three facts convert it into a druggable problem [EV-0044,
EV-0045, EV-0046]: (i) the dominant pathogenic mechanism of the missense class is **protein
destabilization**, i.e. abundance, not active-site chemistry; (ii) kinase catalysis is dispensable for
checkpoint signaling — residual *protein*, even catalytically imperfect, carries function; (iii) the
system is threshold-quantitative — moving residual BUBR1 from ~6%-like toward ~13%-like abundance
changes the phenotype qualitatively. Hence two lever families: **L1, raise the residual mutant protein**
(pharmacological protein-stabilization via the SIRT2–NAD+ axis, which raises BubR1 abundance in vivo and
is named explicitly in the context of MVA [EV-0066], with genetic proof that raising BubR1 is protective
[EV-0067]); and **L2–L4, act on downstream stress axes** (mTORC1-sarcopenia [EV-0057]; aneuploid-cell
clearance [EV-0063]; metabolic/systemic stress [EV-0061, EV-0072]). Notably, no pharmacological SAC
*enhancer* exists anywhere in the literature, and the MPS1/TTK pipeline is entirely inhibitor-direction
(oncology) [EV-0068] — the repurposing space around this node is genuinely open.

---

## 2. Repurposed drug candidates (market-approved only; ranked by reproducible scoring)

Selection pipeline (fully scripted, §5): seed pool of nine mechanism-matched compounds → **automated
marketing-status verification against the openFDA drugsfda API (tier-0)**: six US-approved, three
documented exclusions (NMN, AICAR, 17-AAG — no approved product; exclusion reasons recorded) [EV-0069] →
transparent multi-dimension scoring (`score_candidates.py`; mechanism-match weighted ×2; output in
`candidates_ranked.tsv`). **Four finalists on independent mechanistic axes; two same-axis alternates kept
on record.** This is a research proposal, not a treatment recommendation; every row carries stated
counter-evidence.

| # | Drug | Approval | Axis → chain node | Research hypothesis (abridged) | Key counter-evidence |
|---|---|---|---|---|---|
| 1 | **Niacinamide** | FDA (Rx & OTC products incl. pediatric IV multivitamins) [EV-0069] | L1 protein stability → N5 | Raising NAD+ availability engages SIRT2-dependent stabilization of residual mutant BUBR1, moving abundance toward the fidelity threshold | NMN evidence is from BubR1-insufficient aging mice, not MVA mutants; human RCT endpoint was skin-cancer chemoprevention, not protein abundance [EV-0066 c, EV-0070] |
| 2 | **Metformin** | FDA [EV-0069] | L4 metabolic/systemic stress → N13 | Energy-state modulation ameliorates the metabolic/inflammatory stress component of the aneuploid state | No MVA model data; DS-model endpoints differ; direction-of-effect tension vs L3 (§2.2) [EV-0072 c] |
| 3 | **Chloroquine** | FDA [EV-0069] | L3 aneuploid-cell clearance → N7/N10 | Autophagy inhibition selectively limits proliferation-competence of high-aneuploidy cells, reducing malignant-transformation risk (cancer-prevention scenario) | Cell/MEF-level evidence only; no in vivo tumor-prevention data; pediatric chronic-use retinal toxicity [EV-0063 c] |
| 4 | **Everolimus** | FDA, SEGA indication from age 1 year [EV-0078] | L2 mTORC1-sarcopenia → N11 | mTORC1 inhibition attenuates the sarcopenia/tissue-degeneration component of BUBR1 insufficiency (symptom-domain hypothesis; does not touch segregation fidelity) | Long-term metabolic ADRs (hypercholesterolemia 10/25, T2DM 6/25, hypertension 6/25 in a 15.5-yr pediatric-onset cohort); growth effects in growth-impaired children unstudied [EV-0079] |
| alt | Sirolimus | FDA [EV-0069] | L2 | same axis | shallower pediatric experience than everolimus [EV-0079] |
| alt | Hydroxychloroquine | FDA [EV-0069] | L3 | same axis, better retinal tolerability | zero MVA-model data [EV-0063] |
| ✗ | NMN, AICAR, tanespimycin (17-AAG) | — not approved | — | excluded by the market-approval red line; NMN remains the mechanistic evidence source; 17-AAG additionally mechanism-adverse (HSP90 inhibition destabilizes the very protein L1 tries to stabilize) [EV-0065, EV-0069] |

### 2.1 Niacinamide (axis L1 — the only candidate aimed at the protein-insufficiency node itself)

**Hypothesis (research framing).** In cells expressing the proband's genotype, increased NAD+ availability
enhances SIRT2-mediated deacetylation/stabilization of the residual missense-source BUBR1 protein,
increasing its steady-state abundance toward the ~13% fidelity threshold and away from the ~6%
mis-segregation regime [EV-0044, EV-0045, EV-0046, EV-0066, EV-0067]. The evidence transfer is explicit:
SIRT2 overexpression or the NAD+ precursor NMN raises BubR1 abundance *in vivo* — a study that names MVA
in its translational outlook [EV-0066] — but in BubR1-insufficient aging mice, not MVA missense mutants;
niacinamide is the *market-approved* NAD+ precursor chosen to translate that axis, carrying the stated gap.

**Human precedent at the approved end.** ONTRAC, a phase-3 randomized trial (386 high-risk adults,
500 mg twice daily for 12 months), reduced the rate of new non-melanoma skin cancers by 23% (95% CI 4–38,
P=0.02; SCC −30% P=0.05; BCC −20% P=0.12, not significant) [EV-0070]. We cite this strictly as (a)
proof that systemic nicotinamide at a referenced adult dose alters human cancer incidence and (b) a dose
reference — **not** as evidence of efficacy in MVA, whose tumor biology differs.

### 2.2 Metformin (axis L4) and the direction-of-effect tension, stated openly

Down syndrome (trisomy 21) is the paradigm constitutional aneuploidy, and two tier-1 studies anchor the
metabolic axis: metformin reverses mitochondrial dysfunction in DS cells via the PGC-1α pathway [EV-0072,
Izzo et al. 2017], and AMPK activation is protective across nematode→cellular→mouse DS models [EV-0073].
MVA entails a documented systemic/immune stress component [EV-0061]. The hypothesis is *scenario-limited*:
modulating energy stress to improve stress tolerance of aneuploid-adjacent tissues during development
(function-support scenario). It must not be conflated with Tang's opposite finding that energy stress
(AICAR) **selectively kills** aneuploid cells [EV-0063] — a cancer-prevention scenario. Both directions
are real, cell-autonomy- and context-dependent; our predictions (§3) are scenario-matched, and a failure
to replicate in the worm platform would cleanly falsify the function-support scenario.

### 2.3 Chloroquine (axis L3 — the only candidate with MVA-model evidence)

Tang et al. demonstrated that AICAR, 17-AAG and chloroquine selectively impair the proliferation of
aneuploid cells, **validated on MEFs from BubR1^H/H mice — an MVA model** [EV-0063]. After the approval
filter, chloroquine (and its better-tolerated congener hydroxychloroquine) are the sole market-approved
survivors of that evidence line [EV-0065, EV-0069]. This is a cancer-risk-reduction hypothesis only; it
does not address growth or development, and its evidence ceiling is cell-level.

### 2.4 Everolimus (axis L2 — deepest pediatric precedent, heaviest safety ledger)

The progeroid–sarcopenia branch of BubR1 insufficiency is mTORC1-linked in mice [EV-0057]. Everolimus is
FDA-approved for TSC-associated SEGA from **age 1 year** [EV-0078], with phase-3 RCT and long-term
extension support [EV-0071] and the longest documented pediatric-onset chronic use: median 15.5 years
(max 16.8) in 25 patients, SEGA stable/reduced in 76%, with a defined metabolic ADR profile
(hypercholesterolemia 10, T2DM 6, hypertension 6, osteoporosis 3) [EV-0079]. Those same ADRs, and the
unstudied question of growth in already growth-impaired children, are exactly why this candidate ranks
last among the four despite the strongest regulatory pedigree — the scoring reflects that tension
transparently (§5 script output).

---

## 3. Testable predictions (falsifiability-first)

Primary validation route: the **C. elegans drug-screening/phenotyping platform funded by the MVA Society
itself** [EV-0023]. The worm BUBR1-family homolog is **SAN-1/MAD3**; san-1 and bub-3 deletion mutants are
genome-unstable and stress-hypersensitive [EV-0080] — a direct SAC-weakening surrogate. Each candidate
carries one prediction and one falsification criterion:

| Candidate | Prediction | Falsified if… |
|---|---|---|
| Niacinamide | NAD+ precursor exposure raises BUBR1-family protein abundance and improves stress-tolerance/developmental readouts in san-1/(partial-loss) SAC-weakened worms — readout is protein abundance, not SIRT2 biochemistry (worms lack a clean SIRT2 ortholog) | abundance and phenotype readouts unchanged across dose/time while NAD+ metabolomics confirms target engagement (engagement-shown/no-effect = falsification of the causal step) |
| Metformin | metformin/aak-2-axis activation improves stress-tolerance readouts in the SAC-weakened background (cross-species precedent [EV-0073]) | no improvement, or worsening, in the same scenario that shows protection in trisomy models |
| Chloroquine | organismal-level: reduced proliferative/developmental fitness of SAC-deficient vs wild-type worms under chloroquine (differential sensitivity), consistent with selective burden on the checkpoint-deficient state | no differential (equal sensitivity), undermining selectivity of the effect for the aneuploid state |
| Everolimus | TORC1-pathway manipulation (rapamycin/everolimus; daf-15/Raptor genetics [EV-0074, EV-0081]) improves muscle-function/aging readouts in SAC-weakened worms | muscle/aging readouts unresponsive despite confirmed TORC1 pathway engagement |

Patient-cell route (where samples are available under existing consents): BUBR1 abundance by
quantitative immunoblot/flow in proband lymphocytes before/after ex vivo NAD+ precursor exposure — a
direct pharmacodynamic test of the L1 mechanism.

**Context honesty**: the chloroquine and metformin directions pull against each other at the organism
level; the predictions are deliberately scenario-separated (cancer-prevention vs development-support),
and the worm platform can adjudicate both independently. We commit to reporting null results.

---

## 4. Methods (mapping to official form A7–A17)

- **A7 Team**: JiuTian Bio (single registered participant; disclosure in §0).
- **A8 Approach summary**: controlled genotype → ledger-traced mechanism chain → mechanism-matched
  market-approved drug pool → automated approval verification → transparent scoring → ≤5 ranked
  candidates, each with hypothesis/prediction/counter-evidence.
- **A9 Generative AI**: §0.
- **A10 Automated vs manual**: hybrid. Automated: VCF triage queries, gnomAD remote slices, openFDA
  verification, ledger schema lint, mechanism-chain validation (R1–R6), candidate scoring, read-level variant re-validation, and the
  pre-registered chromosome-level read-depth screen (minimap2→mosdepth→GC-decile + ENCODE-blacklist
  correction, executed on a private dedicated compute node [EV-0083]). Manual:
  literature triage, claim grading, conflict adjudication, all scientific judgments — each recorded with
  source and tier in the ledger.
- **A11 Manual curation detail**: 85-entry evidence ledger; every claim tagged fact/inference/hypothesis/
  strategic_opinion with tier (0–4) and confidence; conflicts carry mandatory conflict-notes (enforced by
  `validate_chain.py` R3/R4 — the validator caught two real issues on first run).
- **A12 Public-only**: **publicly available sources only** — all literature, databases and labels cited
  are public; the controlled dataset was used only for the genotype characterization (§1) permitted by
  the hackathon.
- **A13 Public sources**: ClinVar, gnomAD v4.1 (regional remote slices), Ensembl VEP, PubMed/NCBI
  E-utilities, openFDA (drugsfda + label APIs), ClinicalTrials.gov, Orphanet, OMIM, FDA labels; full
  table with snapshot dates in the repository (`research/evidence.jsonl` per-entry source fields).
- **A14 Proprietary sources**: none.
- **A15 Variant mechanism characterization**: §1.
- **A16 Time and effort**: ≈150 person-hours across Track 1 + Track 2 (literature research, pipeline
  code, evidence ledger curation, validation, raw-read re-validation and lane-level depth screen on a
  dedicated compute node, report drafting; ≈60% of it reading/verification).
- **A17 Abstract**: above.

## 5. Data sources & reproducibility (GitHub)

Repository (made public for review): analysis pipeline `src/track2_repurposing/` —
`ledger.py` (schema lint/stats), `validate_chain.py` (chain×ledger cross-audit R1–R6; `--dot` renders the
mechanism graph), `build_drug_pool.py` (openFDA verification harness), `score_candidates.py` (ranking
reproducing §2). Machine-readable chain: `research/mechanism_chain.json` (14 nodes/15 edges; granularity
tagged public/report). Citation convention: `[EV-xxxx]` refers to the public ledger
(`research/evidence.jsonl`, 85 entries); a small number of entries containing variant- or karyotype-level
detail (e.g., EV-0077, EV-0086) are kept in a private appendix that never enters the public repository, per the
dataset's genomic-data rules — available to organizers on request. All rerunnable from the repository;
controlled genomic data never enters the
repository (gene/domain-level public granularity; transcript-level HGVS appears only in this report
channel). Dataset citation per the Synapse page reference will accompany the published repository
(to be inserted at submission; tracked in the pre-submission checklist) [EV-0082].
Controlled dataset: single-sample WGS (4 lanes, PE150); the raw-read validation and depth screen used
lane L001 — 269M reads, 91.8% properly paired, 13.6% duplicate rate (samtools markdup), ~12× mean
autosomal depth — processed entirely on a
private dedicated compute node [EV-0083, EV-0085, EV-0087].

## 6. Limitations (stated proactively)

1. **Trans configuration is inferred, not directly phased.** The two alleles are >10 kb apart; PE150
   read-backed phasing cannot bridge that distance, and the dataset contains no parental/long-read
   component [EV-0076]. The inference rests on the comp-het architecture rule (null+missense; two nulls
   unreported among survivors) [EV-0047] and official Track 1 confirmation [EV-0042].
2. **The destabilization mechanism is allele-class inference** from transfected-overexpression studies,
   not assayed in patient cells [EV-0044 counter-note]; a minority kinase-activity view exists.
3. Dose thresholds (13%/6%) derive from cell and mouse systems [EV-0046, EV-0050].
4. Cancer penetrance conflicts across sources (38.7% vs ~75%) [EV-0051] — we present the range.
5. No interventional MVA/BUB1B trial has ever been registered [EV-0059] — every candidate is
   first-in-disease by definition; all pediatric safety extrapolations are explicitly flagged (§2.4).
6. Bulk blood WGS cannot resolve a variegated aneuploidy mosaic (single-cell/FISH is the appropriate
   assay); we therefore make no patient-specific aneuploidy-quantification claim. We did test the
   chromosome-scale version of this question under a pre-registered rule: a read-depth screen of one
   lane (100-kb bins; GC-decile correction plus ENCODE-blacklist and N-track masking) found no autosome
   deviating >2% from baseline after correction (1-Mb re-binning concordant), and the weak
   chromosome-level depth signals observed at VCF called sites did not survive correction — adjudicated
   as technical (called-site composition bias). Clonal-gain mosaicism of the hypothesized magnitude
   (10–25%, which would produce a +5–12.5% depth deviation) is excluded; lower-fraction or
   lineage-restricted mosaicism remains untestable in this data type [EV-0085].
7. Worm SAN-1/MAD3 is a homolog, not a one-to-one BUBR1 ortholog (no kinase domain) [EV-0080] — worm
   results translate at pathway level only.
8. Single-patient (N-of-1) evidence base; the proband's nephrocalcinosis remains unexplained [EV-0054].

## 7. Scalability (N-of-1 → N-of-many)

The workflow is deliberately disease-agnostic: (1) controlled genotype + HPO phenotype; (2) mechanism
chain assembled under ledger discipline (every claim graded, conflicts flagged, hypothesis never upgraded
to fact); (3) identify the *druggable property* of an undruggable-looking lesion (here: abundance vs
catalysis; downstream stress axes); (4) market-approval verification by official API (never asserted);
(5) scenario-matched falsifiable predictions in an existing low-cost model platform; (6) commit to null
results. For any rare LoF disease, steps 2–6 reuse verbatim — the ledger, validators and scoring are
already generic code. The bottleneck that remains genuinely human is step 3's scientific judgment.

## 8. License & acknowledgments

This submission is released under **CC-BY 4.0** per hackathon rules.

> *This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with
> the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for
> Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their
> family who generously contributed their data and their story to advance research into this rare
> disease. We acknowledge their trust in making this Hackathon possible.* [EV-0082]

Dataset citation: per the reference provided on the hackathon Synapse page (inserted at submission).
