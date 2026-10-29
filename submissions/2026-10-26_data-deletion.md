# 赛后数据删除留档 · 2026-10-26

## 概要

- 依据：官方细则（讨论 #2，docs/01 §6）+ Rules 页 2026-10-13 更新（EV-0097）；硬期限 ≤2026-11-23。
- 执行手册：docs/19（Step 0–8）。
- 状态：**本机（Mac + SSD）+ 服务器全部删除完成，三处验证通过，确认邮件已送达官方邮箱。**

## 删除时间与执行

- 2026-10-26。Mac + SSD 由助手执行；服务器由用户手动 SSH 执行并确认。

## 位置与对象清单

### 已删除

| 位置 | 对象 | 实测 |
|---|---|---|
| Mac `data/raw/` | WGS VCF + tbi、表型 docx、MANIFEST、`.cache/` | 303 MB |
| Mac `data/processed/` | `bub1b_annotated.vcf.gz(.tbi)`、`bub1b_pass_chr.vcf.gz(.tbi)`（BUB1B 切片，4 文件） | ~60 KB |
| Mac `data/processed/` | `clinical_phenotype.txt`（原始表型全文副本，手册 Step 2 未列，现场补判 DELETE） | — |
| Mac `data/processed/q2_server/return/` | `wg_l001_q2.regions.bed.gz(.csi)`（覆盖度坐标中间表，31134 行，现场补判 DELETE） | 193 KB |
| Mac `data/external/` | `gnomad/`（CEP57/BUB1B/TRIP13 群体频率切片）、`clinvar/`（公共参考 VCF，非患儿数据；为 Step 5 零命中验证一致起见一并删，可随时重下） | 240 MB |
| Mac HF 缓存 | `~/.cache/huggingface/hub/datasets--SageBio--mva-hackathon-2026-data/` | 4 KB 残根 |
| SSD | `/Volumes/SWT9/SageBio/mva-hackathon-2026-data/`（8×FASTQ + VCF + docx 原始交付） | ~85 GB |
| SSD | `/Volumes/SWT9/mva/bam/`（`bub1b_l001.bam` + `.bai`） | 5.2 GB |
| 服务器 | `data/`（L001/L002 FASTQ、q1_targets.tsv）、`out/`（wg_l001.bam、full.dedup.bam、L002 全套 BAM） | 用户确认 |

### 保留（合规 KEEP 类）

- 仓库全部 git 跟踪内容（代码 / docs / 台账 / 提交留档；提交物 CC-BY）。
- docs/16 保护对象 28 项（q1/q2 摘要 JSON、回传包、`candidates_ranked.tsv`、T1 CSV ×2、冻结脚本、基线、私有台账 `evidence_private.jsonl` 等）。
- `data/raw/README.md`、`data/raw/.gitkeep`、`data/external/.gitkeep`（说明文件，无数据）。
- SSD `/Volumes/SWT9/mva/ref/`（GRCh38 公共参考基因组，非赛事数据）。

## Step 5 验证输出

| 检查 | 结果 |
|---|---|
| ① Mac 扫描（data + HF 缓存；vcf/bam/cram/fastq/fq/bcf/sam/tbi/csi） | **0 命中** |
| ② 保护对象 28 项 `shasum -a 256 -c docs/16-保护对象清单-2026-09-17.sha256` | **28/28 OK，0 FAIL** |
| ③ SSD 扫描（fastq/bam/vcf） | **0 命中** |
| ④ 废纸篓 / SSD `.Trashes` / `*.bed.gz`·`regions` 坐标残留 | 无匹配 |
| 服务器核验 | 用户确认 `find` 零命中 + `df -h` 空间已释放 |

## 确认邮件

- 发送时间：2026-10-26 14:28（发件邮箱 = 数据集申请邮箱）。
- **主送 `cnb@sagebase.org`：成功到达对方服务器（2026-10-26 14:28）** ✅
- 抄送 `MVAHackathon2026@synapse.org`：发送失败、已退信（2026-10-26 14:29）。
  - 该地址为数据集门禁表单地址；官方 2026-10-13 已将 Rules 确认地址替换为 `cnb@sagebase.org`（EV-0097），
    退信印证 synapse 侧邮箱已退役。主送送达即满足官方删除确认义务，无需重发（EV-0101）。
- 服务器地址不在此留档（见私有 `data/processed/project_state_2026-09-17.md`，不入公开仓库）。

## 后续触发点

- 11-20 09:00 兜底核验（docs/19 Step 8）：重跑三处扫描 + 废纸篓 + 全盘 SSD 扫描。
- 仓库保持 public 至 ≥2026-12-18 获奖公布（EV-0099）。

## 2026-10-29 追记：官方提醒邮件复核（EV-0102/0103，Step 8 扩展版提前执行）

- 收到官方两封邮件并入账：删除提醒（EV-0102，明示 prompts/logs、git 历史、权重等此前未逐项列出的核对项）
  与我方确认邮件的官方回执（EV-0103）——**删除确认义务至此获官方回执闭环**，synapse 抄送退信无影响。
- 对照 EV-0102 删除清单逐项复核（2026-10-29，全绿，**无需补删**）：

| 核对项（EV-0102 明示） | 结果 |
|---|---|
| Mac / SSD / HF 缓存 / 废纸篓 / Downloads / Desktop / /tmp 基因组文件（含索引） | 0 命中（仅 `tools/snpEff` 自带公共示例 VCF，非赛事数据）；Time Machine 本地快照无 |
| 保护对象 28 项 `shasum -c` | 28/28 OK（当日复验） |
| 存储的 prompts/logs（Claude 会话 ×7 + 子代理 ×1 + 输入历史 + llm-usage.log + 交叉审查 dry_run/输出 + zsh 历史） | 基因型数值（`0/1:23,5` 式）**0 处**、VCF 数据行 **0 行**；模式命中均为审签哈希（AD=xxx）/ git-blob 扫描器正则代码 / 台账格式描述文字；裸坐标 ≤11 处 = 已公开提交物候选变异（官方 finding 级，保留合法） |
| git 全历史 | 无任何基因组文件 blob；文本命中仅 EV-0035 格式描述行 → **无需 filter-repo** |
| 权重 / embedding / 微调 | 无（全项目未在原始数据上训练） |
| 基因组级中间表残留（q2_server / track2 / cross_review 逐文件扫描） | 0 命中（均为摘要 JSON / 脚本 / 结论级） |
| 队友各自确认 | 不适用（单人队伍，数据集门禁仅限本人） |

- 新增 watch items：12-18 获奖后须配合**税务文件 + 制裁筛查**（奖金发放前置条件，EV-0102）；
  11-20 兜底核验按 docs/19 Step 8 + 本节新增两项（prompts/logs、git 历史）执行。
