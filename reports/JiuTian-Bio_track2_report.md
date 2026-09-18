# Track 2 Proposal — Repurposing Market-Approved Drugs for Mosaic Variegated Aneuploidy Syndrome Type 1 (BUB1B)

**Team**: JiuTian Bio · **Submitter**: millerkai · **Date**: 2026-09 (v1) · **Track**: 2 — Drug Repurposing

> Evidence discipline: every substantive claim in this report cites an entry number (EV-xxxx) from our
> evidence ledger (`research/evidence.jsonl` in the accompanying repository). Tier-0 sources are
> official pages/rules/labels/source code; tier-1 are peer-reviewed literature. Conflicts between sources are
> flagged inline, not smoothed over. All drug statements are **research hypotheses with testable predictions
> and stated counter-evidence** — nothing in this document is a treatment recommendation.

---

## 0. Generative-AI disclosure (required)

> **Recorded tools: Anthropic Claude via Claude Code (initial workflow); OpenAI Codex desktop (subsequent review and revisions); DeepSeek and Qwen API sessions plus one manual ChatGPT (Deep Research) session for independent cross-review — public-tier materials only.**

The initial workflow used Claude Code for variant triage, literature search assistance, coding,
and drafting. The usage log records that workflow as using a commercial Anthropic API plan.
Subsequent Codex desktop sessions assisted with code review, synthetic tests, interpretation of
returned diagnostic summaries, transfer tooling, and report revisions. Tool-visible material included
private target scripts and historical notes containing variant-level information; this was not an
exclusively public-material workflow. Safeguards: private material remained within
participant-controlled compute environments; LLM services were restricted to Processor-type terms (no
training, no data-rights acquisition, time-limited retention) as a selection condition, and no third
party was granted data access. Per-service term verification is closed as of 2026-09-17:
API providers (Anthropic commercial API, DeepSeek, Qwen) were checked against their published
terms at selection and at each review batch, and the OpenAI account used for the ChatGPT and
Codex sessions had account Data Controls (model-training opt-in) disabled, confirmed against the
account settings by the participant (account-side settings are participant-verified, not
independently auditable; per-session Codex model versions were not logged).
Server computations were executed by the participant.
The ledger is the permitted source for scientific report claims; automated citation checks do not
replace source-level human review. Independent cross-review was completed on 2026-09-17 —
citation audit, mechanism-chain/ledger consistency, rules-language, medical-wording, and
predictive-validity reviews across the services above, with human adjudication of every
adopt/reject decision and documented rejections. The claims registry (`research/report_claims.tsv`)
records all report claims as independently reviewed, with a hash-bound attestation
(`research/review_attestations.jsonl`). Residual limitation, stated plainly: the independent
reviewers were LLM services from providers other than the drafting tools, plus participant
adjudication — not external domain-expert peer review. The log records no submission of model
outputs for vendor scoring or feedback. Data interactions are inventoried in `docs/llm-usage.log`.

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
repurposing question unanswered by the field: with **zero** registered interventional trials for
MVA/BUB1B (ClinicalTrials.gov query), which *market-approved* drugs act on nodes of this chain — as
research hypotheses, not treatment options?
Because BUBR1 loss is not classically druggable, we targeted two properties: (i) the pathogenic
model emphasizes **abundance**, with a mechanism shown only
in BubR1-insufficient aging mice (not MVA mutants) by which BUBR1 abundance might be raised via the
SIRT2–NAD+ axis; (ii) downstream stress axes (mTORC1-associated sarcopenia, aneuploid-cell metabolic stress,
selective aneuploid-cell clearance) are druggable with approved compounds. From a seed pool of nine
mechanism-matched compounds, automated openFDA screening found marketed records for six; subsequent
product-level review **excluded niacinamide at the market-approval gate** — the only verified FDA record
is a combination multivitamin, not a matching single-ingredient product [EV-0088]. A
penalty-aware research-priority score with prespecified eligibility and direction-veto rules — a
falsification-priority ordering, not an efficacy or benefit ranking — shortlisted two research hypotheses
on independent axes: **everolimus** (mTORC1 axis; direct product and the closest disease-model evidence bridge in the
eligible set, still untested in MVA),
**metformin** (energy-stress modulation; DS-cell mitochondrial data only).
**Chloroquine is listed only as a high-risk mechanistic probe, not a finalist**: its trisomic-MEF
effect may represent toxicity to non-transformed aneuploid tissue, and no selective window has been
shown. Each hypothesis carries a falsifiable prediction — primarily in the *C. elegans* SAC-weakening platform (san-1/MAD3, the worm BUBR1-family homolog), plus patient-cell readouts
— and the counter-evidence that could refute the hypothesis (evidence-transfer gaps, pediatric
safety burdens, and a direction-of-effect tension between "clear aneuploid cells" and
"support aneuploid-cell fitness", separated by clinical scenario). All drug statements here are
falsifiable research hypotheses, not treatment recommendations. **Strengths**: ledger-linked
claims with structural checks, source-grading, conflict disclosure, and market-approval
verification by official API. **Limitations**: the compound-heterozygous *trans*
configuration is inferred (direct read overlap did not establish phase; chained phasing was not assessed);
the destabilization mechanism is inferred from the allele class rather than assayed in patient cells;
dose thresholds derive from cell/mouse systems; and no candidate has been tested in MVA. This framework —
controlled genotype → ledger-enforced mechanism chain → mechanism-matched approved-drug ranking →
falsifiable predictions — offers a framework for rare-disease N-of-1 analysis.

---

## 1. Variant mechanism characterization (form A15; submission-page hard requirement)

### 1.1 Genotype (report-level granularity)

The proband carries the two-variant **BUB1B** answer confirmed by the official Track 1 full match
([EV-0042]); trans configuration remains inferred (see §6) — phase was not directly tested, and the
mechanistic reasoning in §1–§3 is explicitly conditioned on this inference. Variant-level coordinates,
alleles, HGVS, residue positions, and read counts are confined to the controlled private appendix
[EV-0039, EV-0040].

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
genotype architecture of the reported MVA1 case series — truncating allele paired with a
kinase-domain missense allele, with complete-null genotypes absent from those series and from our
2026-09-08 search of later reports (an absence-based observation consistent with mouse knockout
embryonic lethality, not a permanent exclusion) [EV-0047].

### 1.2 Mechanistic chain (LoF character; pathway disrupted; downstream consequences)

```
N1  BUB1B variant pair (nonsense + missense; trans inferred)
 ├── N2  nonsense allele → predicted NMD / functional-null hypothesis [EV-0039, EV-0048]
 │        (annotation plus evidence from other patients/alleles; not measured in this proband)
 ├── N3  missense allele → protein destabilization (5–10× lower abundance,                 (inference from
 │        proteasomal clearance, HSP90-dependent folding; kinase activity dispensable)      allele class)
 │        [EV-0040, EV-0044, EV-0045]
 ↓  (reported architecture pattern: truncating + kinase missense [EV-0047])
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
 (from N5) N14 druggable stability axis: SIRT2–NAD+ deacetylase control of BubR1 abundance
 │       (inference; evidence from BubR1-insufficient aging mice, not MVA mutants) [EV-0066, EV-0067]
```

Per-node grading (fact / inference / hypothesis) is maintained in the machine-readable chain
(`research/mechanism_chain.json`); nodes carrying population- or model-level evidence into this
proband's chain (N4, N7, N9, N11, N13, N14) are graded inference, not fact. The JSON file is the
authoritative grading source.

**HPO alignment of the proband's 8 phenotype terms**: 6/8 map strongly onto the chain (rhabdomyosarcoma→N10,
short stature / failure to thrive / SGA→N8, muscle atrophy→N11, parental RPL→N9); prematurity aligns
indirectly (no published MVA–prematurity analysis; plausible via placental insufficiency, stated as such);
**our PubMed search found no published MVA/BUB1B–nephrocalcinosis
association** (absence-based, as of 2026-09-08), and it is reported honestly as an unexplained
observation, not a mechanism claim [EV-0054]. The ciliopathy hypothesis for MVA remains directly
contradicted in the literature [EV-0053 conflict] and is not used.

### 1.3 Why BUB1B loss is "undruggable" — and what is actually druggable

BUBR1 loss of function looks like a classical undruggable problem: one cannot agonize a missing
tumor-suppressor-like checkpoint protein. Three facts convert it into a druggable problem [EV-0044,
EV-0045, EV-0046]: (i) the dominant pathogenic mechanism of the missense class is **protein
destabilization**, i.e. abundance, not active-site chemistry; (ii) kinase catalysis is dispensable for
checkpoint signaling — residual *protein*, even catalytically imperfect, carries function; (iii) the
system is threshold-quantitative in models — directionally, moving residual BUBR1 abundance out of the
mis-segregation regime toward the fidelity-preserving regime changes the phenotype qualitatively (the
~13%/~6% thresholds are model-derived, not measured in this proband [EV-0046]). Conversely, if the
minority kinase-activity view of allele 2 [EV-0044] were correct, lever L1 would fail mechanistically —
adding abundance of a catalysis-defective protein would not restore function under that model. Hence two
lever families: **L1, raise the residual mutant protein**
(pharmacological protein-stabilization via the SIRT2–NAD+ axis, which raises BubR1 abundance in vivo —
in BubR1-insufficient aging mice, not MVA mutants — and names MVA explicitly in its translational outlook
[EV-0066]; genetic proof that raising BubR1 is protective [EV-0067]); and **L2–L4, act on downstream stress axes** (mTORC1-sarcopenia [EV-0057]; aneuploid-cell
clearance [EV-0063]; metabolic/systemic stress [EV-0061, EV-0072]). Notably, our search
(re-verified 2026-09-17) found no validated small molecule shown to restore a weakened BUB1B/SAC
checkpoint — reported pharmacological SAC activators act by perturbing mitosis rather than correcting
checkpoint insufficiency [EV-0093, EV-0094] — and the MPS1/TTK pipeline is entirely
inhibitor-direction (oncology) [EV-0068]; within that search, the repurposing space around this node
is open.

---

## 2. Repurposing screen (eligible products, conditional hypotheses, and documented exclusions)

Selection pipeline (§5): seed pool → openFDA component-level screen [EV-0069] → manual product-level FDA
label review [EV-0088] → penalty-aware research-priority scoring from a tracked TSV. The score separates
disease-model evidence, direct target engagement, testability, human exposure, pediatric feasibility,
translation distance, and counter-evidence severity. It is **not** an efficacy, clinical-benefit, or
risk-benefit score. Five prespecified illustrative weight scenarios report limited rank sensitivity;
they do not establish universal robustness. Same-axis compounds remain
alternates even when their numeric priority is high. Niacinamide fails the product-level market-approval
gate — its only verified record is a combination product [EV-0088] — and is therefore excluded from the
nomination table (mechanistic rationale retained in §2.1; re-enters only if a matching direct marketed
product is verified).

| # | Drug | Score | Approval | Axis → chain node | Research hypothesis (abridged; not treatment advice) | Key counter-evidence |
|---|---|---|---|---|---|---|
| 1 | **Everolimus** | 14 (rank 1–1) | Direct FDA product; approved for TSC-associated SEGA (age ≥1 yr) — pediatric exposure precedent only, not an MVA indication [EV-0078, EV-0088] | L2 mTORC1-sarcopenia → N11 | Hypothesis from mouse models: mTORC1 inhibition may attenuate the sarcopenia/tissue-degeneration component (never tested in MVA) | No MVA-model or MVA-patient data exist; documented metabolic ADRs in pediatric TSC cohorts (hypercholesterolemia/T2DM/hypertension/osteoporosis [EV-0079]); growth velocity in already growth-impaired children unstudied [EV-0079] |
| 2 | **Metformin** | 7 (rank 4–4 overall) | Direct FDA product [EV-0088] | L4 metabolic/systemic stress → N13 | Energy-state modulation may alter the metabolic/inflammatory stress component in either direction (model-system data only; scenario-dependent, untested in MVA) | No MVA-model data; DS evidence is single-layer (fetal fibroblasts, mitochondrial endpoints — no growth or cancer endpoints; no cross-species aneuploidy chain [EV-0072, EV-0073 correction]); the DS→MVA transfer carries an explicit causal gap (uniform trisomy vs mosaic aneuploidy); the direction of effect may oppose the aneuploid-cell-clearance strategy (L3), and which direction dominates in a developing organism is unknown [EV-0072, EV-0063] |
| high-risk probe | **Chloroquine** | 3 (rank 5–5 overall) | Direct FDA product [EV-0088] | L3 aneuploid-cell fitness → N7/N10 | Probe hypothesis (in vitro only; not a treatment, not a nomination): a mammalian cell-triplet assay would test whether any tumor-versus-non-transformed selectivity window exists | Hard veto: the known direction may worsen loss of non-transformed aneuploid cells; no BubR1 CQ experiment or in-vivo prevention data [EV-0063] |
| alt | Sirolimus | 12 (rank 2–3) | Direct FDA product [EV-0088] | L2 | High numeric priority but same axis as everolimus | shallower pediatric context and immunosuppression burden [EV-0079] |
| alt | Hydroxychloroquine | −2 (rank 6–6) | Direct FDA product [EV-0088] | L3 | same axis | no Tang MEF data [EV-0063] |
| ✗ | Niacinamide | 10 (rank 2–3; ineligible) | component-only: INFUVITE PEDIATRIC combination [EV-0088] | L1 protein stability → N5 | excluded by the market-approval red line — no verified matching single-ingredient systemic product; mechanistic rationale retained for hypothesis-testing only (§2.1); transfers: NMN→niacinamide chemistry, aging-mouse→MVA-mutant biology [EV-0066, EV-0088] | exclusion at left; transfer-gap counter-evidence in §2.1 |
| ✗ | NMN, AICAR, tanespimycin (17-AAG) | — | — not approved | — | excluded by the market-approval red line; NMN remains the mechanistic evidence source; 17-AAG additionally mechanism-adverse (HSP90 inhibition destabilizes the very protein L1 tries to stabilize) [EV-0065, EV-0069] | not applicable — not approved; exclusion at left |

*Table note*: "Score" is the penalty-aware research-priority score — an ordering of falsification work,
not of expected benefit, efficacy, or preference; same-axis "alt" rows are alternates, not additional
nominations.

### 2.1 Niacinamide (axis L1 — excluded from nomination by the market-approval gate)

**Hypothesis (research framing; not a treatment recommendation).** We hypothesize that in an in-vitro
assay of cells expressing the proband's genotype, increased NAD+ availability would enhance SIRT2-mediated
deacetylation/stabilization of the residual missense-source BUBR1 protein,
increasing its steady-state abundance directionally — toward the fidelity-preserving regime of the
cell-model dose series and away from the mis-segregation regime (thresholds model-derived, not measured
in this proband) [EV-0044, EV-0045, EV-0046, EV-0066, EV-0067]. The evidence transfer is explicit:
SIRT2 overexpression or the NAD+ precursor NMN raises BubR1 abundance *in vivo* — a study that names MVA
in its translational outlook [EV-0066] — but in BubR1-insufficient aging mice, not MVA missense mutants;
the L1 rationale is therefore carried as an untranslated mechanism hypothesis — and niacinamide itself
stands excluded from nomination until a matching market-approved single-ingredient product is verified
[EV-0088].

**Product-status limitation.** The verified FDA record is INFUVITE PEDIATRIC, an intravenous combination
multivitamin in which niacinamide is one component; it does not establish a matching single-ingredient
systemic product or the proposed exposure [EV-0088]. ONTRAC, a phase-3 randomized trial in 386 high-risk adults, reported a reduction in the rate of new
non-melanoma skin cancers [EV-0070] (effect size, CI, and subgroup statistics are recorded in the ledger
entry and deliberately not reproduced here, to avoid any misreading as an efficacy or dosing reference).
We cite this strictly as (a)
proof that systemic nicotinamide exposure has been studied in adults — **not** as evidence of efficacy,
a dose proposal for MVA, or a pediatric testing dose.

### 2.2 Metformin (axis L4) and the direction-of-effect tension, stated openly

Down syndrome (trisomy 21) is the paradigm constitutional aneuploidy. One tier-1 study anchors the
metabolic axis: metformin reverses mitochondrial dysfunction in DS cells via the PGC-1α pathway [EV-0072,
Izzo et al. 2017]. A second cross-species AMPK study, catalogued in our ledger as DS, was shown by
independent citation review (2026-09-17) to study Huntington's-disease models instead (nematode →
mutant-Htt striatal cells → mouse; ledger corrected) [EV-0073]. We retain it only as evidence that
AMPK-driven stress protection is pharmacologically engageable across species, and state the resulting
gap plainly: our sources contain no cross-species aneuploidy-model chain for this axis — the DS
evidence is a single layer (fetal fibroblasts).

The DS→MVA transfer carries an explicit causal gap: DS is a uniform constitutive trisomy, whereas MVA1 is
random, mosaic aneuploidy arising from checkpoint leakage in a subset of cells. Three differences follow:
(a) cell autonomy — every DS cell is aneuploid versus a variegated subset; (b) timing — congenital uniform
stress versus ongoing mis-segregation; (c) stress quality — dosage-balance stress versus the mixed
proteotoxic/mitotic stress of random gains and losses. The shared substrate is cellular-stress
physiology — mitochondrial stress in trisomy cells [EV-0072] and AMPK-responsiveness in non-aneuploidy
cross-species models [EV-0073] — not a shared cause; the axis is therefore treated as exploratory in
MVA — which is precisely what the worm prediction tests.

MVA entails a documented systemic/immune stress component [EV-0061]. The hypothesis is *scenario-limited*
and model-bound: modulating energy stress might improve stress tolerance of aneuploid-adjacent tissues
during development (function-support scenario). It must not be conflated with Tang's opposite finding that energy stress
(AICAR) **selectively kills** aneuploid cells [EV-0063] — a cancer-prevention scenario. Both directions
are real, cell-autonomy- and context-dependent; our predictions (§3) are scenario-matched, and a failure
to replicate in the worm platform would cleanly falsify the function-support scenario. The scenarios are
separated analytically, not independently actionable: a developing organism runs both directions at once,
so any margin between aneuploid-tissue support and aneuploid-cell clearance is a timing/dose question the
platform itself would have to map.

### 2.3 Everolimus (axis L2 — deepest pediatric precedent, heaviest safety ledger)

The progeroid–sarcopenia branch of BubR1 insufficiency is mTORC1-linked in mice [EV-0057]. The following
TSC/SEGA figures are cited solely as pediatric exposure and ADR precedent, not as expected benefit in
MVA. Everolimus is FDA-approved for TSC-associated SEGA from **age 1 year** [EV-0078], with phase-3 RCT
and long-term extension support [EV-0071] and a very long documented pediatric-onset chronic-use cohort: median
15.5 years (max 16.8) in 25 patients, with a defined metabolic ADR profile (hypercholesterolemia 10,
T2DM 6, hypertension 6, osteoporosis 3) [EV-0079] (SEGA-response figures are recorded in the ledger
[EV-0079] and not reproduced here — they concern the TSC indication and have no bearing on MVA). Those
same ADRs, and the
unstudied question of growth in already growth-impaired children are explicit penalties. Two evidence
components are kept apart: direct target engagement (everolimus inhibits mTORC1 — a product-level fact)
versus the disease-model bridge (the BubR1-insufficiency mouse sarcopenia axis — an inference from a model
system, not an MVA observation). The revised research-priority rubric weighs both, assigning this hypothesis the highest
falsification-priority score (14; rank 1 under all five weight scenarios) — an
ordering of which hypothesis to test first, not a ranking of expected benefit. The TSC pediatric experience transfers at the level of pharmacokinetics and the documented ADR
spectrum in young children; it does not transfer at the level of efficacy mechanism — SEGA control is
mTORC1-driven hamartoma growth, not checkpoint-insufficiency sarcopenia. A null muscle/aging result
despite confirmed TORC1 engagement (§3) would falsify the MVA-side mechanism specifically; the PK/ADR
knowledge would remain valid and simply irrelevant to it.

### 2.4 Chloroquine (axis L3 — high-risk mechanistic probe, not a finalist)

Tang et al. identified AICAR, 17-AAG and chloroquine as selectively impairing proliferation of
**trisomic MEFs** [EV-0063]. The follow-up experiment on SAC-compromised MEFs (BubR1^H/H, an MVA
model, and Cdc20^AAA) tested **AICAR and 17-AAG only** (Tang 2011 Fig. 6A–B); chloroquine was not
assayed in that system [EV-0063]. After the approval filter, chloroquine (and hydroxychloroquine)
are the direct-product survivors of that paper's hit list [EV-0065, EV-0088]. Translation distance and
counter-evidence are now explicit penalties, producing a research-priority score of 3 (stable overall
rank 5 across five illustrative weight scenarios). A safety/direction hard veto prevents finalist
selection: reduced fitness of non-transformed aneuploid cells could aggravate tissue loss in MVA, and no
tumor-versus-normal MVA-tissue selectivity window has been established. The first experiment must therefore compare
diploid control, non-transformed BUB1B-deficient, and transformed cells; differential toxicity alone is
not a positive therapeutic result. Hydroxychloroquine is excluded by the same veto and additionally
lacks the cited MEF experiment.

---

## 3. Testable predictions (falsifiability-first)

Primary validation route: the **C. elegans drug-screening/phenotyping platform funded by the MVA Society
itself** [EV-0023] (platform funding is not an endorsement of or association with this report). The worm
BUBR1-family homolog is **SAN-1/MAD3**; san-1 and bub-3 deletion mutants are
genome-unstable and stress-hypersensitive [EV-0080] — a direct SAC-weakening surrogate. Each nominated
candidate — plus the L1 mechanism test (niacinamide, excluded from nomination, §2.1) — carries one
prediction and one falsification criterion (nomination = selection for falsification work, not
selection of a drug for use):

| Research hypothesis | Prediction (experiment design) | Falsified if… |
|---|---|---|
| Niacinamide (L1 mechanism test; excluded from nomination, §2.1) | predicted, in *C. elegans* only: NAD+ precursor addition to the worm culture (research reagent, not a supplement) raises BUBR1-family protein abundance and improves stress-tolerance/developmental readouts in san-1/(partial-loss) SAC-weakened worms — readout is protein abundance, not SIRT2 biochemistry (worms lack a clean SIRT2 ortholog) | abundance and phenotype readouts unchanged across dose/time while NAD+ metabolomics confirms target engagement (engagement-shown/no-effect = falsification of the causal step) |
| Metformin | predicted, in *C. elegans* only: metformin/aak-2-axis activation improves stress-tolerance readouts in the SAC-weakened background (AMPK stress-response precedent from non-aneuploidy models [EV-0073]) | no improvement, or worsening, in the worm analog of the DS-cell mitochondrial rescue (DS cells only, not MVA; no cross-species aneuploidy chain exists [EV-0072]) |
| Everolimus | predicted, in *C. elegans* only: TORC1-pathway manipulation (rapamycin/everolimus; daf-15/Raptor genetics [EV-0074, EV-0081]) improves muscle-function/aging readouts in SAC-weakened worms | muscle/aging readouts unresponsive despite confirmed TORC1 pathway engagement — an efficacy-mechanism failure that TSC PK/ADR experience cannot bridge (§2.3) |

Chloroquine's criterion is **not executable in the worm platform** (no tumors — platform mismatch): it
requires an in-vitro mammalian cell-line triplet — diploid control, non-transformed BUB1B-deficient,
and transformed cells — with no in-vivo or patient testing, to ask whether any
tumor-versus-non-transformed **selectivity window** exists; differential
toxicity alone is not a positive result.

Patient-cell route (in vitro laboratory assay only; where samples are available under existing
consents): BUBR1 abundance by quantitative immunoblot/flow in proband lymphocytes cultured ex vivo with
and without a research-grade NAD+ precursor added to the culture dish only (no compound is
administered to the patient) — a pharmacodynamic assay of the L1 mechanism only, not a treatment, an
in-vivo exposure, or a suggestion to administer anything.

**Context honesty**: the chloroquine and metformin directions pull against each other at the organism
level; the predictions are deliberately scenario-separated (cancer-prevention vs development-support).
The worm platform adjudicates the metformin-side scenario; chloroquine's selectivity question requires
the mammalian cell triplet above. We commit to reporting null results.

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
- **A12 Public-only**: public sources plus the hackathon-licensed controlled dataset, used only for the
  genotype characterization (§1) as the hackathon permits; all literature, databases and labels cited are
  public, and no controlled material enters the public repository or submission.
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
(to be inserted at submission; tracked in the pre-submission checklist) [EV-0082]. Per the rules, all raw
and genome-derivable data will be deleted within 30 days of the hackathon close, confirmed by email to
the designated official addresses, and no manuscript using this dataset will be submitted during the
embargo period.
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
5. As of 2026-09-17 (independently re-verified during cross-review via the ClinicalTrials.gov API), no
   interventional MVA/BUB1B trial is registered on ClinicalTrials.gov [EV-0059] — every candidate is
   first-in-disease within that registry; all pediatric safety extrapolations are explicitly flagged (§2.1–2.4).
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
   baseline threshold in 300/300 simulated replicates for each nominated chromosome [EV-0085] — an
   internal sensitivity property of the pipeline against its own observed baseline, not evidence about
   the proband's true karyotype. This
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
already generic code.

**Retrospective positive-control walkthrough (TSC–SEGA).** To check that the six steps run on a
disease that is not this proband's, we walked them against a rare-disease repurposing outcome already
represented in our ledger: everolimus for tuberous-sclerosis-complex subependymal giant cell
astrocytoma (TSC-SEGA). (1) Controlled genotype: TSC is caused by loss-of-function mutations in TSC1
or TSC2 [EV-0095]. (2) Mechanism chain: two nodes — loss of the TSC protein complex's inhibition of
mTOR signalling [EV-0095]. (3) Druggable property: where MVA presents a missing protein to be
stabilized, the TSC lesion is pathway over-activation, directly inhibitor-addressable — the framework
surfaces this difference instead of promising equal difficulty. (4) Approved-drug screen: mTOR
inhibitors with direct FDA products [EV-0088]. (5) Falsifiable prediction: SEGA volume response in a
randomized trial — EXIST-1 [EV-0071]. (6) Post-approval long-term pediatric safety monitoring
[EV-0079]. No step used MVA-specific machinery. The honest reading is not that our pipeline "would
have discovered" everolimus — TSC had assets MVA lacks (an inhibitor-addressable lesion and a
measurable primary endpoint) — but that the workflow runs end-to-end on an independent disease and
correctly locates the added difficulty in step 3's scientific judgment. This is a methods-level
scalability check, not an analysis of TSC.

The bottleneck that remains genuinely human is step 3's scientific judgment.

## 8. License & acknowledgments

This submission is released under **CC-BY 4.0** per hackathon rules.

> *This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with
> the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for
> Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their
> family who generously contributed their data and their story to advance research into this rare
> disease. We acknowledge their trust in making this Hackathon possible.* [EV-0082]

Dataset citation: per the reference provided on the hackathon Synapse page (inserted at submission).
