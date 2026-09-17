# Track 2 — Drug Repurposing (MVA1 / BUB1B)

T2 主战场模块。核心资产是**机器可读机制链 + 证据台账**。自动校验检查报告中的 EV 引用、
机制链和已登记 claim 的结构；不能证明清单覆盖每条断言，也不能证明文献支持其句意。
这只是 M5 对抗审查门的自动化部分。

## 文件

| 文件 | 阶段 | 作用 |
|---|---|---|
| `ledger.py` | M1–M3 | 台账 CLI：`lint`（schema 关卡）/ `stats` / `show` / `grep` |
| `validate_chain.py` | M1 | 机制链 × 台账交叉审计（R1–R6 规则，详见文件头）；`--dot` 可出机制图 |
| `build_drug_pool.py` | M2 | openFDA 成分级初筛；`api_error` 整跑失败，不能替代产品级标签复核 |
| `score_candidates.py` | M2 | 跟踪 TSV × 产品表 → 研究优先级与五场景敏感性；不是疗效分数 |
| `depth_power.py` | M2 | 相对观测样本的追加乘性信号恢复与 block-bootstrap 分离；不提供生物学排除界限 |
| `research/mechanism_chain.json` | M1 | 机制链本体（nodes 带 ev_refs / granularity / conflict_note） |

## 运行

```bash
.venv/bin/python src/track2_repurposing/ledger.py lint
.venv/bin/python src/track2_repurposing/validate_chain.py
.venv/bin/python src/track2_repurposing/validate_chain.py --dot   # 机制图 DOT
.venv/bin/python src/track2_repurposing/score_candidates.py --check-only # 只读比对既有排名
```

两道关卡全绿是 M5 放行的前置条件。

`score_candidates.py` 不带 `--check-only` 时会生成排名文件；综合 preflight 只用只读模式。
公开代码尚未覆盖完整 Q2 历史执行链；比对、GC 分箱、原裁决脚本目前仍在私有区。
冻结 Q1 validator 的已知限制和历史注释更正见 `server_tasks/q1_full_reference_recheck/README.md`。

## 数据与存储约定（2026-09-08 定）

- **本模块不依赖原始测序数据**：79GB FASTQ 本机磁盘放不下，T2 主体走「文献 + 台账 + 公开药物数据库」
- SSD 接入后（用户操作）的可选增强：FASTQ 下载 → 比对 → read-backed 定相（验证 comp-het trans），
  以及全基因组注释链（任务 #9，冻结中，仅机制章需要时解冻）——全部落到 SSD，路径约定
  `/Volumes/<SSD>/mva/`，仓库内只留指针与结论级产物
- 基因组级文件永不入 git（.gitignore 已兜底）；公开 repo 口径 = 基因/结构域级
  （机制链 JSON 中 `granularity=report` 的内容只进提交报告，不进公开仓库）

## 阶段与验收（对应任务 #11–#16，详见 docs/07）

M1 机制链定稿（validate_chain 全绿）→ M2 药池+评分（≤5 精选，三件套齐全）→
M3 报告成稿（11 问骨架，摘要 ≤500 词）→ M4 视频 → M5 对抗审查门（本模块两关卡 + 子代理三查）→
M6 两段式提交（10 月上旬 v1 占坑 → ≤10/20 终版）。
