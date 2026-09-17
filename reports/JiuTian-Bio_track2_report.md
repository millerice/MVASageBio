# Track 2 Proposal — Repurposing Market-Approved Drugs for Mosaic Variegated Aneuploidy Syndrome Type 1 (BUB1B)

**Team**: JiuTian Bio · **Submitter**: millerkai · **Date**: 2026-09 (v1) · **Track**: 2 — Drug Repurposing

> Evidence discipline: every substantive claim in this report cites an entry number (EV-xxxx) from our
> evidence ledger (`research/evidence.jsonl` in the accompanying repository). Tier-0 sources are
> official pages/rules/labels/source code; tier-1 are peer-reviewed literature. Conflicts between sources are
> flagged inline, not smoothed over. All drug statements are **research hypotheses with testable predictions
> and stated counter-evidence** — nothing in this document is a treatment recommendation.

---

## 0. Generative-AI disclosure (required)

> **Recorded tools: Anthropic Claude via Claude Code; OpenAI Codex desktop for subsequent review and revisions.**

The initial workflow used Claude Code for variant triage, literature search assistance, coding,
and drafting. The usage log records that workflow as using a commercial Anthropic API plan.
Subsequent Codex desktop sessions assisted with code review, synthetic tests, interpretation of
returned diagnostic summaries, transfer tooling, and report revisions. Tool-visible material included
private target scripts and historical notes containing variant-level information; this was not an
exclusively public-material workflow. Server computations were executed by the participant.
The ledger is the permitted source for scientific report claims; automated citation checks do not
replace source-level human review. Final independent review, the complete interaction inventory,
and account-specific service-term verification remain pending. This draft does not attest that all
claims have received completed human verification or that every service session has passed a
Processor-terms audit. The initial log records no submission of model outputs for vendor scoring
or feedback. Data interactions and remaining disclosure checks are recorded in `docs/llm-usage.log`.

## Abstract (form A17; strengths and limitations included)

Mosaic variegated aneuploidy (MVA) syndrome type 1 is caused by biallelic loss-of-function of **BUB1B**,
encoding the spindle assembly checkpoint (SAC) kinase BUBR1. In the proband of this hackathon dataset we
identified a variant pair with inferred trans configuration: a nonsense allele in an NMD-sensitive exon
(a functional-null hypothesis [EV-0039, EV-0048]) paired with a kinase-domain missense allele interpreted from its class as a
**protein-destabilizing hypomorph** — MVA1 kinase-domain missense mutants reduce BUBR1 protein abundance
5–10× via proteasomal clearance, while kinase catalysis itself is dispensable for checkpoint signaling.
The proposed BUBR1-insufficiency mechanism links SAC weakening to aspects of the phenotype;
expression thresholds derive from experimental models and neither allele's functional effect has
been measured in this proband [EV-0044, EV-0046, EV-0048]. We assembled this
mechanism as a machine-readable, ledger-traced chain (14 nodes, every claim source-graded), and asked a
repurposing question the field has not yet answered: with **zero** registered interventional trials for
MVA/BUB1B (ClinicalTrials.gov, tier-0 query), which *market-approved* drugs act on nodes of this chain?
Because BUBR1 loss is not classically druggable, we targeted two non-obvious properties: (i) the pathogenic
model emphasizes **abundance**, with an experimental route to raising BUBR1 abundance via the
SIRT2–NAD+ axis; (ii) downstream stress axes (mTORC1-driven sarcopenia, aneuploid-cell metabolic stress,
selective aneuploid-cell clearance) are druggable with approved compounds. From a seed pool of nine
mechanism-matched compounds, automated openFDA screening found marketed records for six; subsequent
product-level review made **niacinamide conditional rather than a finalist**, because the verified FDA
product is a combination multivitamin rather than a matching single-ingredient product [EV-0088]. A
penalty-aware research-priority score plus prespecified manual eligibility and direction-veto rules—not
an efficacy score—selected two eligible candidates on
independent axes: **everolimus** (mTORC1 axis; direct product and the closest disease-model bridge),
**metformin** (energy-stress modulation with cross-species protection in aneuploidy models).
**Chloroquine is retained only as a high-risk mechanistic probe, not a finalist**: its trisomic-MEF
effect may represent toxicity to non-transformed aneuploid tissue, and no therapeutic window has been
shown. For each hypothesis
we state a falsifiable prediction — primarily in the *C. elegans* SAC-weakening platform that the MVA
Society itself funds (san-1/MAD3 is the worm BUBR1-family homolog), plus patient-cell biomarker readouts
— and the specific counter-evidence that could refute the hypothesis (evidence-transfer gaps, pediatric
safety burdens, and one acknowledged direction-of-effect tension between "clear aneuploid cells" and
"support aneuploid-cell fitness", which we separate by clinical scenario). **Strengths**: ledger-linked
claims with automated structural checks, source-grading, conflict disclosure, and market-approval
verification by official API rather than assertion. **Limitations**: the compound-heterozygous *trans*
configuration is inferred (direct read overlap did not establish phase; chained phasing was not assessed);
the destabilization mechanism is inferred from the allele class rather than assayed in patient cells;
dose thresholds derive from cell/mouse systems; and no candidate has been tested in MVA. This framework —
controlled genotype → ledger-enforced mechanism chain → mechanism-matched approved-drug ranking →
falsifiable predictions — offers a framework for rare-disease N-of-1 analysis.

---

## 1. Variant mechanism characterization (form A15; submission-page hard requirement)

### 1.1 Genotype (report-level granularity)

The proband carries the two-variant **BUB1B** answer confirmed by the official Track 1 full match
([EV-0042]); trans configuration remains inferred (see §6). Variant-level coordinates, alleles, HGVS,
residue positions, and read counts are confined to the controlled private appendix [EV-0039, EV-0040].

| Allele | Public-safe class | Mechanistic interpretation |
|---|---|---|
| 1 | Nonsense | NMD-sensitive **functional-null hypothesis** [EV-0039, EV-0048] |
| 2 | Rare missense in the kinase-domain region | **Destabilizing-hypomorph hypothesis**, inferred from the allele class rather than measured in patient cells [EV-0040, EV-0044, EV-0045] |

Public-safe supporting observations are limited to conclusion level: one allele has authoritative
pathogenic/likely-pathogenic database support and the other is population-rare with damaging in-silico
predictions [EV-0039, EV-0040]. Both loci had heterozygous support in the source VCF [EV-0077]. A
controlled-server full-reference follow-up assessed lanes L001 and L002 separately. After duplicate
removal, one candidate passed in both lanes; the other did not meet the support threshold in either lane
[EV-0089]. Before duplicate removal, both passed in L001, whereas the second candidate already had
insufficient ALT support and an ALT fraction below the specified range in L002. Exploratory balance and
orientation tests did not detect nominally significant departures, but limited evidence and unadjusted
post-hoc tests do not establish absence of bias. The original support thresholds and the later-added
zero-mate-conflict criterion were reported separately. Library relationships remain unverified; no joint
deduplication was performed. These observations neither establish absence of the second candidate nor
constitute orthogonal validation. Direct read overlap did not establish phase; chained phasing was not
assessed [EV-0089]. The official Track 1 full match establishes agreement with the answer key, not
independent biological validation [EV-0042]. This variant architecture (predicted truncating null + kinase-domain missense) resembles the
published rule for surviving MVA1 — two complete nulls have never been reported [EV-0047].

### 1.2 Mechanistic chain (LoF character; pathway disrupted; downstream consequences)

```
N1  BUB1B variant pair (nonsense + missense; trans inferred)
 ├── N2  nonsense allele → predicted NMD / functional-null hypothesis [EV-0039, EV-0048]
 │        (annotation plus evidence from other patients/alleles; not measured in this proband)
 ├── N3  missense allele → protein destabilization (5–10× lower abundance,                 (inference from
 │        proteasomal clearance, HSP90-dependent folding; kinase activity dispensable)      allele class)
 │        [EV-0040, EV-0044, EV-0045]
 ↓  (architecture rule: truncating + kinase missense [EV-0047])
 N5  proposed BUBR1 protein INSUFFICIENCY in the proband (model-derived dose dependence)
 │     ~13% expression → segregation fidelity preserved; ~6% → mis-segregation in most cells [EV-0046]
 │     mouse dose series: progeroid/dwarfism/cancer at low dose, massive apoptosis at very low dose [EV-0050]
 ↓
 N6  SAC weakening: insufficient MCC–APC/C inhibition → shortened mitosis, PSCS [EV-0044, EV-0049, EV-0055]
 ↓
 N7  MOSAIC VARIEGATED ANEUPLOIDY (~25–50% of patient cells random gains/losses) [EV-0049, EV-0055]
 ↓ ↓ ↓ ↓  (four phenotype branches)
 ├─ N8  growth failure: progenitor apoptosis → tissue hypoplasia (93.5% of MVA patients) [EV-0050, EV-0051, EV-0055]
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

## 2. Repurposing screen (eligible products, conditional hypotheses, and documented exclusions)

Selection pipeline (§5): seed pool → openFDA component-level screen [EV-0069] → manual product-level FDA
label review [EV-0088] → penalty-aware research-priority scoring from a tracked TSV. The score separates
disease-model evidence, direct target engagement, testability, human exposure, pediatric feasibility,
translation distance, and counter-evidence severity. It is **not** an efficacy, clinical-benefit, or
risk-benefit score. Five prespecified illustrative weight scenarios report limited rank sensitivity;
they do not establish universal robustness. Same-axis compounds remain
alternates even when their numeric priority is high. Niacinamide remains a mechanistically interesting
conditional hypothesis but is not a finalist unless a matching direct marketed product is verified.

| # | Drug | Score | Approval | Axis → chain node | Research hypothesis (abridged) | Key counter-evidence |
|---|---|---|---|---|---|---|
| 1 | **Everolimus** | 14 (rank 1–1) | Direct FDA product; SEGA from age 1 [EV-0078, EV-0088] | L2 mTORC1-sarcopenia → N11 | mTORC1 inhibition may attenuate the sarcopenia/tissue-degeneration component | Long-term metabolic ADRs and growth uncertainty [EV-0079] |
| 2 | **Metformin** | 7 (rank 4–4 overall) | Direct FDA product [EV-0088] | L4 metabolic/systemic stress → N13 | Energy-state modulation may alter the metabolic/inflammatory stress component | No MVA-model data; DS endpoints differ; direction tension vs L3 [EV-0072] |
| high-risk probe | **Chloroquine** | 3 (rank 5–5 overall) | Direct FDA product [EV-0088] | L3 aneuploid-cell fitness → N7/N10 | First test whether any tumor-versus-non-transformed MVA-tissue window exists | Hard veto: the known direction may worsen loss of non-transformed aneuploid cells; no BubR1 CQ experiment or in-vivo prevention data [EV-0063] |
| conditional | **Niacinamide** | 10 (rank 2–3) | **Component-only evidence**: INFUVITE PEDIATRIC combination product [EV-0088] | L1 protein stability → N5 | Test whether a market-eligible NAD+ precursor can stabilize residual BUBR1 | Two major transfers and no matching direct product yet [EV-0066, EV-0088] |
| alt | Sirolimus | 12 (rank 2–3) | Direct FDA product [EV-0088] | L2 | High numeric priority but same axis as everolimus | shallower pediatric context and immunosuppression burden [EV-0079] |
| alt | Hydroxychloroquine | −2 (rank 6–6) | Direct FDA product [EV-0088] | L3 | same axis | no Tang MEF data [EV-0063] |
| ✗ | NMN, AICAR, tanespimycin (17-AAG) | — | — not approved | — | excluded by the market-approval red line; NMN remains the mechanistic evidence source; 17-AAG additionally mechanism-adverse (HSP90 inhibition destabilizes the very protein L1 tries to stabilize) [EV-0065, EV-0069] | — |

### 2.1 Niacinamide (axis L1 — conditional hypothesis, not currently a finalist)

**Hypothesis (research framing).** In cells expressing the proband's genotype, increased NAD+ availability
enhances SIRT2-mediated deacetylation/stabilization of the residual missense-source BUBR1 protein,
increasing its steady-state abundance toward the ~13% fidelity threshold and away from the ~6%
mis-segregation regime [EV-0044, EV-0045, EV-0046, EV-0066, EV-0067]. The evidence transfer is explicit:
SIRT2 overexpression or the NAD+ precursor NMN raises BubR1 abundance *in vivo* — a study that names MVA
in its translational outlook [EV-0066] — but in BubR1-insufficient aging mice, not MVA missense mutants;
niacinamide is therefore retained only as a conditional translation hypothesis, carrying the stated gap.

**Product-status limitation.** The verified FDA record is INFUVITE PEDIATRIC, an intravenous combination
multivitamin in which niacinamide is one component; it does not establish a matching single-ingredient
systemic product or the proposed exposure [EV-0088]. ONTRAC, a phase-3 randomized trial (386 high-risk adults,
500 mg twice daily for 12 months), reduced the rate of new non-melanoma skin cancers by 23% (95% CI 4–38,
P=0.02; SCC −30% P=0.05; BCC −20% P=0.12, not significant) [EV-0070]. We cite this strictly as (a)
proof that systemic nicotinamide exposure has been studied in adults — **not** as evidence of efficacy,
a dose proposal for MVA, or a pediatric testing dose.

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

### 2.3 Everolimus (axis L2 — deepest pediatric precedent, heaviest safety ledger)

The progeroid–sarcopenia branch of BubR1 insufficiency is mTORC1-linked in mice [EV-0057]. Everolimus is
FDA-approved for TSC-associated SEGA from **age 1 year** [EV-0078], with phase-3 RCT and long-term
extension support [EV-0071] and the longest documented pediatric-onset chronic use: median 15.5 years
(max 16.8) in 25 patients, SEGA stable/reduced in 76%, with a defined metabolic ADR profile
(hypercholesterolemia 10, T2DM 6, hypertension 6, osteoporosis 3) [EV-0079]. Those same ADRs, and the
unstudied question of growth in already growth-impaired children are explicit penalties. Under the
revised research-priority rubric, direct target engagement and the BubR1-insufficiency mouse bridge make
this the highest-ranked eligible hypothesis (14; rank 1 under all five weight scenarios). This ranking
means priority for falsification, not expected patient benefit.

### 2.4 Chloroquine (axis L3 — high-risk mechanistic probe, not a finalist)

Tang et al. identified AICAR, 17-AAG and chloroquine as selectively impairing proliferation of
**trisomic MEFs** [EV-0063]. The follow-up experiment on SAC-compromised MEFs (BubR1^H/H, an MVA
model, and Cdc20^AAA) tested **AICAR and 17-AAG only** (Tang 2011 Fig. 6A–B); chloroquine was not
assayed in that system [EV-0063]. After the approval filter, chloroquine (and hydroxychloroquine)
are the direct-product survivors of that paper's hit list [EV-0065, EV-0088]. Translation distance and
counter-evidence are now explicit penalties, producing a research-priority score of 3 (stable overall
rank 5 across five illustrative weight scenarios). A safety/direction hard veto prevents finalist
selection: reduced fitness of non-transformed aneuploid cells could aggravate tissue loss in MVA, and no
tumor-versus-normal MVA-tissue window has been established. The first experiment must therefore compare
diploid control, non-transformed BUB1B-deficient, and transformed cells; differential toxicity alone is
not a positive therapeutic result. Hydroxychloroquine is excluded by the same veto and additionally
lacks the cited MEF experiment.

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
| Chloroquine (high-risk probe) | establish a tumor-versus-non-transformed therapeutic window across diploid control, non-transformed BUB1B-deficient, and transformed backgrounds; worm fitness loss alone counts as toxicity, not benefit | no tumor-selective window, or disproportionate harm to non-transformed BUB1B-deficient cells |
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
  drug pool → automated component screen plus manual product-label verification → penalty-aware research-priority scoring → ≤5 ranked
  candidates, each with hypothesis/prediction/counter-evidence.
- **A9 Generative AI**: §0.
- **A10 Automated vs manual**: hybrid. Automated: VCF triage queries, gnomAD remote slices, openFDA
  component screening, ledger schema lint, mechanism-chain validation, priority-score sensitivity analysis, raw-read support re-evaluation, and the
  pre-registered chromosome-level read-depth screen (minimap2→mosdepth→GC-decile + ENCODE-blacklist
  correction, executed on a private dedicated compute node [EV-0083]). Manual:
  literature triage, claim grading, conflict adjudication, all scientific judgments — each recorded with
  source and tier in the ledger.
- **A11 Manual curation detail**: evidence ledger with claims tagged fact/inference/hypothesis/
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

Repository materials intended for public review: analysis pipeline `src/track2_repurposing/` —
`ledger.py` (schema lint/stats), `validate_chain.py` (chain×ledger×claim-manifest cross-audit; `--dot`
renders the mechanism graph), `build_drug_pool.py` (openFDA component-screening harness), and
`score_candidates.py` (tracked scoring inputs, penalties, and five-scenario rank sensitivity).
Machine-readable chain: `research/mechanism_chain.json` (14 nodes/15 edges; granularity
tagged public/report). Citation convention: `[EV-xxxx]` refers to the public ledger
(`research/evidence.jsonl`); a small number of entries containing variant- or karyotype-level
detail (e.g., EV-0077, EV-0086) are kept in a private appendix that never enters the public repository, per the
dataset's genomic-data rules. Sharing remains subject to the original access restrictions.
Reproducibility is partial: the current workspace includes scoring and validation code, while the
historical Q2 alignment, GC-bin generation, and original adjudication scripts remain in private,
gitignored storage. Complete execution provenance linking server scripts, inputs, and BAMs is still
being audited; current code hashes alone cannot establish which code ran historically. Controlled genomic data never enters the
repository (gene/domain-level public granularity only; no coordinates, alleles, HGVS, read counts, or
karyotype-level measurements appear in public artifacts). Dataset citation per the Synapse page reference will accompany the published repository
(to be inserted at submission; tracked in the pre-submission checklist) [EV-0082].
Controlled dataset: single-sample WGS (4 lanes, PE150); the initial read-support check and depth screen used
lane L001 — 269M reads, 91.8% properly paired, 13.6% duplicate rate (samtools markdup), ~12× mean
autosomal depth — processed entirely on a
private dedicated compute node [EV-0083, EV-0085, EV-0087]. The subsequent Q1 follow-up additionally
analyzed L002 separately; the L001 QC figures above must not be attributed to L002 [EV-0089].

## 6. Limitations (stated proactively)

1. **Trans configuration is inferred, not directly phased.** Direct qualified read-name overlap did not
   establish phase; chained phasing was not assessed [EV-0089]. The dataset contains no parental/long-read
   component [EV-0076]. Disease architecture motivates the trans hypothesis [EV-0047]; official Track 1
   agreement with the answer key is not direct phase evidence [EV-0042].
2. **Both allele mechanisms remain inferred in this proband.** The functional-null hypothesis combines
   annotation with transcript findings in other patients/alleles [EV-0039, EV-0048]. The destabilization
   hypothesis derives from allele-class studies, including transfected-overexpression systems, rather
   than this proband's cells [EV-0044]; a minority kinase-activity view exists.
3. Dose thresholds (13%/6%) derive from cell and mouse systems [EV-0046, EV-0050].
4. Cancer penetrance conflicts across sources (38.7% vs ~75%) [EV-0051] — we present the range.
5. No interventional MVA/BUB1B trial has ever been registered [EV-0059] — every candidate is
   first-in-disease by definition; all pediatric safety extrapolations are explicitly flagged (§2.4).
6. Bulk blood WGS cannot resolve random cell-to-cell variegated aneuploidy (single-cell/FISH is the
   appropriate assay); we therefore make no patient-wide MVA-karyotype claim. We tested only whether
   the specific chromosome-wide signals nominated from VCF called sites reproduced in one-lane read
   depth. After 100-kb binning, GC-decile correction, and ENCODE-blacklist/N-track masking,
   the nominated signals did not survive the
   pre-registered >15% rule. This non-replication is consistent with called-site composition or other
   ascertainment bias; it does not prove one unique artifact mechanism. Because that original
   threshold alone could not exclude smaller effects, we added a clearly post hoc sensitivity
   analysis: 300 one-megabase block-bootstrap replicates with +2.5% to +15% additional chromosome-wide
   effects injected before GC-decile correction. The smallest added effect exceeded the empirical
   baseline threshold in 300/300 simulated replicates for each nominated chromosome [EV-0085]. This
   measures separation of an added signal from the observed baseline. That baseline is not an
   independently calibrated biological no-gain null; the legacy output name `detection_power` is not
   the power of the original fixed-threshold screen. Systematic bias is not identified by these
   resamples. The historical depth pipeline did not first mark duplicates or explicitly raise the
   MAPQ threshold; sensitivity to those choices remains untested [EV-0085]. These simulations do
   **not** establish a biological exclusion bound for stable gains, low-fraction, tissue-restricted,
   or random cell-to-cell MVA karyotypes.
7. Worm SAN-1/MAD3 is a homolog, not a one-to-one BUBR1 ortholog (no kinase domain) [EV-0080] — worm
   results translate at pathway level only.
8. Single-patient (N-of-1) evidence base; the proband's nephrocalcinosis remains unexplained [EV-0054].

## 7. Scalability (N-of-1 → N-of-many)

The workflow is deliberately disease-agnostic: (1) controlled genotype + HPO phenotype; (2) mechanism
chain assembled under ledger discipline (every claim graded, conflicts flagged, hypothesis never upgraded
to fact); (3) identify the *druggable property* of an undruggable-looking lesion (here: abundance vs
catalysis; downstream stress axes); (4) component screening followed by product-level label verification;
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
