# MVASageBio — MVA 黑客松 2026 参赛项目

[Sage Bionetworks "rare-disease-real-kid-mva-hackathon-2026"](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026)：基于一名真实 MVA 患儿的 WGS 数据，完成变异预测（T1）与药物重定位（T2）。

## 快速链接

| 资源 | 地址 |
|---|---|
| 比赛主页（提交/榜单/讨论） | https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026 |
| 数据集（gated，需申请） | https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data |
| T1 评分参考论文（Stenton 2024, CAGI6-RGP） | https://doi.org/10.1186/s40246-024-00604-w |
| 官方模板（提交 CSV / methods 表） | Space 内 Submit 页下载，或 `static/templates/` |
| **截止时间** | **2026-10-24 23:59 UTC**（~7.5 周） |

## 文档索引（赛前摸底报告 + 架构）

1. [00 · 项目架构与工作流](docs/00-项目架构与工作流.md) — 双赛道流水线设计与仓库结构
2. [01 · 赛制摸底](docs/01-赛制摸底.md) — 规则/提交格式/评分算法（源码级）/合规
3. [02 · 战况分析](docs/02-战况分析.md) — 榜单态势与社区情报
4. [03 · 疾病背景](docs/03-疾病背景.md) — MVA/BUB1B 机制与治疗格局（T2 弹药库）
5. [04 · 机会点与策略](docs/04-机会点与策略.md) — 战场选择、打法、时间表
6. [05 · 里程碑准出门槛](docs/05-里程碑准出门槛.md) — 各阶段验收检查单（Exit Gates）

另有：`CLAUDE.md`（项目指令：合规红线/证据规则/医学安全/技术速查）、`research/evidence.jsonl`（证据台账，报告引用 EV 编号）。

## 核心结论（30 秒版）

- T1 满分已遍地（官方预期内）→ 快速拿满分，**重仓 methods 报告**
- **T2 是官方明示的价值洼地** → 主战场（Rigor 35% / Impact 25% / Innovation 25% / Scalability 15%）
- 答案是 **comp-het 双变异**（官方评分源码确认）→ 管线按隐性模型设计；头号嫌疑 BUB1B（=MVA 1 型，非 2 型；2 型是 CEP57）
- 🌟 创新/社区奖独立于名次 → 患者为中心的交付物单独冲这条线

## 状态

- [x] 赛前调研（本目录 docs/）
- [x] 目录骨架与工作流框架
- [x] CLAUDE.md 项目指令 + 证据台账（41 条 EV）+ 里程碑准出门槛（G3 增机制链对抗审查）
- [x] 本地评分 harness（`src/track1_variant/`：官方内核 import + 提交前校验，23 项测试全绿）+ LLM 使用日志建档
- [x] **数据权限获批 + 选择性下载**（2026-09-08：VCF/tbi/临床表型 docx/README 共 302.8MB，sha256 校验一致；FASTQ 79GB 暂缓——磁盘与定相策略见 EV-0033）
- [x] **T1 v0 候选锁定**（2026-09-08：BUB1B comp-het 双变异，ClinVar P/LP + 私有错义；CEP57/TRIP13 排除；本地 scorer 满分预检；方法报告 `reports/t1_methods_v0.md`；提交留档 `submissions/`）——待线上首次提交
- [ ] T1 线上提交 → 满分确认
- [ ] T2 报告 + 视频

## 合规速记（违者出局项）

数据 30 天内删除并邮件确认 · 不 recontact 家庭/MVA Society · 不转发数据 · LLM 按 Processor 配置并在 methods 披露 · GitHub 评审时公开 · T2 只提名已上市药物 · 提交 CC-BY
