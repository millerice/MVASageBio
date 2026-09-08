# Track 1 Methods Report — v0

**Team**: MVASageBio · **Date**: 2026-09-08 · **Track**: T1 Variant Prediction

> 按比赛数据使用条款，本公开方法报告不包含先证者变异级基因型数据；候选变异仅通过官方提交表单的 CSV 通道提交。疾病基因层面的结论（基因符号、解读逻辑）依据 CC-BY 发布。

## 1. Data

| 项 | 值 |
|---|---|
| 数据 | 官方受控 WGS VCF（单样本，未定相，无功能注释） |
| 参考基因组 | GRCh38 |
| 变异规模 | 5,012,204 变异 / 4,740,790 PASS（QC 后全量统计） |
| 临床输入 | 官方临床表型文档，提取 8 个 HPO 词条（含横纹肌肉瘤、早产/小于胎龄、复发性流产家族史） |

## 2. Pipeline（S1→S6）

1. **QC**：全量统计（变异数、PASS 率、SNV/indel 构成、合子状态分布）；确认 contig 无 `chr` 前缀（提交打包时统一转换）。
2. **基因优先级**：以 MVA（mosaic variegated aneuploidy）已知致病基因为主集——BUB1B（MVA1）、CEP57（MVA2）、TRIP13（MVA3），依据 OMIM 分型与表型吻合度排序。
3. **区域注释**：对候选基因全基因区间（±5 kb）逐一提取先证者 PASS 变异，按基因区域远程拉取 gnomAD v4.1 sites 切片（AF/AC/AN、CADD、REVEL、SpliceAI、VEP 后果）并合并；ClinVar（GRCh38 VCF）全注释。
4. **comp-het 判定**：在候选基因内寻找"双杂合 + 双稀有 + 双功能后果"组合：等位基因频率阈值 AF < 0.01（LoF 更严）、后果等级 HIGH/MODERATE、评分佐证（CADD/SpliceAI/REVEL；私有变异用 Ensembl VEP 的 SIFT/PolyPhen）。
5. **鉴别排除**：CEP57、TRIP13 基因区间经同一管线注释后无编码区变异命中，均排除。
6. **打包预检**：本地评分 harness（直接 import 官方 `evaluation.py` 内核）对提交 CSV 做 preflight + 满分路径模拟，确认格式/前缀/配对无误。

## 3. Tools

- bcftools/htslib 1.24（区域提取、注释合并、基因型质控）
- gnomAD v4.1 sites（按基因区域切片）、ClinVar VCF（NCBI，2026-09 快照）
- Ensembl VEP REST（私有变异后果与 HGVS）
- 本地评分 harness（官方 evaluation.py 原内核 + 23 项单元测试）

## 4. Interpretation criteria

- ClinVar 致病性评级（含评审星级）为第一证据层；
- gnomAD v4.1 基因组 AF 稀有性（含 faf95、人群最大 AF、nhomalt）为第二层；
- 后果等级（stop-gain/missense/splice）+ NMD 敏感性（外显子位置）为第三层；
- 错义变异需 ≥2 个独立预测算法一致（SIFT/PolyPhen）；
- 表型一致性（BUB1B-MVA 与横纹肌肉瘤的已知关联）作为先验而非独立证据。

## 5. Limitations

- VCF 未定相且无父母样本：双杂合变异的 trans 配置基于超稀有双打击的贝叶斯推理，未直接定相验证；
- 未做 read-backed 定相（数据集无 BAM，比对因磁盘与算力暂缓）；
- 未评估结构变异/CNV（VCF 仅含 SNV/indel）；
- epcr 为团队主观后验估计。

## 6. LLM 使用披露（比赛条款要求）

本项目的分析管线设计、代码实现与文档写作中使用了 LLM（Anthropic Claude Code，Processor 型服务，不用于模型训练）。所有生物学结论均经人工复核并溯源至证据台账（ClinVar / gnomAD / OMIM / Ensembl 等公开数据库），LLM 未产生未经数据库佐证的生物学断言。提交数据仅含变异坐标，不含原始测序数据。

## 7. License

本报告按比赛要求以 CC-BY 4.0 发布。
