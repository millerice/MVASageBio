# 参考资料

## 官方资源

- 比赛主页：https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026
- 数据集（gated）：https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data
- 官方源码（评分/提交逻辑，本次调研已全文捕获）：
  - `evaluation.py` — T1 评分算法（rank tiers、comp-het 半分、F-max）
  - `config.py` — 配额（T1×6 / T2×3）、榜单数据集
  - `submit_track1.py` / `submit_track2.py` — 提交表单与格式要求
  - `rules.py` / `tabs/about.py` / `tabs/faq.py` — 规则全文
  - 提交模板：`static/templates/track1_submission_template.csv`、`methods_description_form.xlsx`
- 关键讨论帖：
  - [#18 Track 1 Leaderboard 公告](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/18)（战况核心证据）
  - [#10 Hackathon Updates](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/10)（T2 配额 1→3 等）
  - [#2 第三方 LLM 使用裁决](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2)（Processor/Recipient 判定）
  - [#17 参考基因组确认 GRCh38](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/17)

## T1 方法论文献

- Stenton et al. 2024, Human Genomics — CAGI6-RGP 评估方法（rank points / EPCR / F-max 的原型）：https://doi.org/10.1186/s40246-024-00604-w
- Exomiser（表型驱动变异优先级，开源基线）：https://exomiser.github.io/
- gnomAD：https://gnomad.broadinstitute.org/
- REVEL / CADD / AlphaMissense / SpliceAI — 变异危害预测注解

## 疾病背景（详见 docs/03-疾病背景.md）

- MVA Society：https://mvasociety.org/
- OMIM 257300（MVA1/BUB1B）：https://omim.org/entry/257300
- Orphanet MVA：https://www.orpha.net/en/disease/detail/1052
- Suijkerbuijk et al. 2010（BUBR1 与 MVA）：https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/
- MalaCards MVA1（comp-het 致病）：https://www.malacards.org/card/mosaic_variegated_aneuploidy_syndrome_1

## T2 药物重定位数据库

- Open Targets：https://www.opentargets.org/
- DGIdb（drug-gene interaction）：https://dgidb.org/
- DrugBank：https://go.drugbank.com/
- LINCS L1000 / CLUE（签名反转）：https://clue.io/
- Broad Drug Repurposing Hub：https://www.broadinstitute.org/drug-repurposing-hub
- CTD（比较毒理基因组）：https://ctdbase.org/
