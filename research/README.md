# 证据台账（Evidence Ledger）

`evidence.jsonl` — 每行一条 JSON（EV 条目）。本项目所有关键结论的可追溯根基，也是 T2 报告 Scientific Rigor（权重 35%）的直接素材来源。

## 字段定义

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | `EV-0001` 起递增，永不复用 |
| `domain` | enum | `competition` / `battlefield` / `disease` / `therapy` / `strategy` |
| `claim` | string | 结论本身，一句话可判定 |
| `claim_type` | enum | `fact` / `inference` / `hypothesis` / `strategic_opinion` |
| `tier` | int | 来源等级 0–4，定义见根目录 `CLAUDE.md` |
| `source` | object | `{title, url, publisher, published_date, retrieved_at}` |
| `evidence` | string | 支撑该结论的原文要点 / 数据 |
| `counter_evidence` | string? | 反面证据（鼓励填写——主动列反证是 T2 评审加分项） |
| `confidence` | float | 0–1 |
| `verification_status` | enum | `verified` / `unverified` / `conflict` |
| `notes` | string? | 备注（冲突检测说明、待办验证等） |

## 使用规则

1. **先入账再引用**：关键 claim 写入报告/提交物前必须在台账中存在，引用格式 `[EV-XXXX]`
2. **Reporter 隔离**：终版报告只准引用已入账条目。公开台账 = `research/evidence.jsonl`；位点/核型级私有附录 = `data/processed/evidence_private.jsonl`（gitignored，当前 ID：EV-0077、EV-0086 及 EV-0039/0040 的坐标级全文）。公开报告可写 `[EV-0077]`，数值留私有附录。两种都算台账；`-private` 后缀不是合法 ID。
3. **不擅自升格**：`hypothesis` 不得写成 `fact`，除非新证据入账并复核
4. **冲突处理**：发现矛盾 → 新建条目标 `conflict` → notes 说明 → 解决后更新状态
5. **合规**：台账只存结论级内容（属官方删除规则的 KEEP 类），禁止存任何基因组级基因型数据
6. **终版审计**：T1/T2 提交前，由子代理对抗审查——每条关键结论 → EV 编号存在且 `verification_status=verified`

## 当前覆盖

首批 24 条（2026-09-02 建账）：

| 域 | 条目 | 说明 |
|---|---|---|
| competition | EV-0001 ~ 0013 | 赛制 13 条（答案结构/评分/配额/合规/时间线/奖金），全部 Tier 0 |
| battlefield | EV-0014 ~ 0016 | 战况 3 条（官方公告、满分情报核对、社区 LLM 态度） |
| disease | EV-0017 ~ 0023 | 疾病 7 条（基因分型/癌症风险/BUBR1 生物学/治疗格局） |
| strategy | EV-0024 | 头号假设：答案为 BUB1B comp-het（待数据验证） |

追加（2026-09-08，评分源码细读 + harness 建档）：

| 域 | 条目 | 说明 |
|---|---|---|
| competition | EV-0025 ~ 0030 | 评分算法细节（排序规则 / full-match 判定 / F-max 扫描 / 变异规范化 chr 前缀敏感）与提交表单硬校验（GitHub URL + 报告必填）、答案键存放位置；全部 Tier 0，经 hf-mirror 镜像获取、SHA256 留档 `references/official/README.md` |
| competition | EV-0031 ~ 0032 | 数据访问获批与门禁条款留档；删除确认邮箱两官方来源不一致（conflict → 双发兜底） |
| competition / disease | EV-0033 ~ 0038 | 数据集勘察：构成/无 chr 前缀陷阱/GRCh38+GATK 元数据/8 个 HPO 词条（含父母流产史）；表型对 BUB1B 假说的独立支持（inference）；镜像源码官方复核 7/7 |
| disease / competition | EV-0039 ~ 0041 | **T1 破案**：BUB1B 无义杂合（ClinVar P/LP·MVA1）+ 私有错义杂合 comp-het 候选（公开版已脱敏至基因级，完整版在受控私有台账 `data/processed/evidence_private.jsonl`）；gnomAD v4.1 远程切片策略与基础设施事实 |

`therapy` 域条目随 T2 的 M1–M4 阶段补充（候选药物 schema：drug / target / mechanism / evidence / counter_evidence / pediatric_relevance / confidence / status）。
